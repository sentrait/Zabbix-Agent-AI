import os
import logging
import json
from typing import Dict, Any, List
from .zabbix_service import zabbix_service
from .config_service import config_service

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self._load_config()
        
        # Define available tools
        self.tools = [
            {
                "name": "create_host",
                "description": "Create a new host in Zabbix. ONLY use this after gathering all necessary info (OS, Templates, Interface).",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "host_name": { "type": "string", "description": "The visible name of the host" },
                        "ip_address": { "type": "string", "description": "The IP address of the host" },
                        "group_id": { "type": "string", "description": "The ID of the host group." },
                        "template_ids": { "type": "array", "items": {"type": "string"}, "description": "List of Template IDs to link." },
                        "description": { "type": "string", "description": "Description of the host's purpose." },
                        "interface_type": { "type": "integer", "description": "1=Agent, 2=SNMP, 3=IPMI, 4=JMX. Default 1." },
                        "port": { "type": "string", "description": "Port number. Default 10050." }
                    },
                    "required": ["host_name", "ip_address", "group_id"]
                }
            },
            {
                "name": "get_templates",
                "description": "Search for Zabbix Templates by name. Use to find correct template IDs for the host OS.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "search": { "type": "string", "description": "Search term (e.g. 'Linux', 'Windows', 'Cisco')." }
                    },
                    "required": ["search"]
                }
            },
            {
                "name": "get_host_groups",
                "description": "Get a list of available host groups in Zabbix. Use this to help find the correct group_id.",
                "input_schema": {
                    "type": "object", 
                    "properties": {}, 
                    "required": []
                }
            },
            {
                "name": "acknowledge_problem",
                "description": "Acknowledge a problem in Zabbix. Use this when the user wants to take ownership of an alert or leave a comment.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "event_id": { "type": "string", "description": "The Event ID or precise Name of the problem to acknowledge." },
                        "message": { "type": "string", "description": "The comment or message to leave on the problem." }
                    },
                    "required": ["event_id", "message"]
                }
            },
            {
                "name": "schedule_maintenance",
                "description": "Put a host into maintenance mode immediately for a specified duration. This suppresses alerts.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "host_id": { "type": "string", "description": "The Host ID or Hostname to put in maintenance." },
                        "minutes": { "type": "integer", "description": "Duration of maintenance in minutes." },
                        "description": { "type": "string", "description": "Reason for maintenance." }
                    },
                    "required": ["host_id", "minutes"]
                }
            },
            {
                "name": "update_host_status",
                "description": "Enable or disable monitoring for a specific host.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "host_id": { "type": "string", "description": "The Host ID or Hostname." },
                        "status": { "type": "string", "enum": ["0", "1"], "description": "0 to Enable/Monitor, 1 to Disable/Stop Monitoring." }
                    },
                    "required": ["host_id", "status"]
                }
            }
        ]

    def _load_config(self):
        config = config_service.get_config()
        self.provider = config.get("provider", "bedrock")
        self.aws_region = config.get("aws_region", "us-east-1")
        self.aws_access_key = config.get("aws_access_key")
        self.aws_secret_key = config.get("aws_secret_key")
        self.bedrock_model_id = config.get("bedrock_model_id", "us.anthropic.claude-3-5-sonnet-20241022-v2:0")
        self.openai_api_key = config.get("openai_api_key")
        self.openai_model = config.get("openai_model", "gpt-4o")
        self.gemini_api_key = config.get("gemini_api_key")
        self.gemini_model = config.get("gemini_model", "gemini-1.5-pro-latest")

    def chat(self, message: str, context: Dict[str, Any] = None) -> str:
        self._load_config() # Reload config on every request to pick up changes
        
        try:
            if self.provider == "bedrock":
                return self._chat_bedrock(message, context)
            elif self.provider == "openai":
                return self._chat_openai(message, context)
            elif self.provider == "gemini":
                return self._chat_gemini(message, context)
            else:
                return f"Error: Unknown provider '{self.provider}'"
        except Exception as e:
            logger.error(f"Chat Error ({self.provider}): {e}", exc_info=True)
            return f"Error connecting to AI service ({self.provider}): {str(e)}"

    def _chat_bedrock(self, message: str, context: Dict[str, Any] = None) -> str:
        if not os.getenv("BEDROCK_API_KEY") and not (self.aws_access_key and self.aws_secret_key):
             return "AI Configuration Error: AWS credentials not configured."

        import boto3
        
        # Configure Boto3 client
        if self.aws_access_key and self.aws_secret_key:
            bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region,
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key
            )
        elif os.getenv("BEDROCK_API_KEY"):
             os.environ['AWS_BEARER_TOKEN_BEDROCK'] = os.getenv("BEDROCK_API_KEY")
             bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region
            )
        else:
             # Fallback to default credentials chain
             bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=self.aws_region
            )

        system_prompt = self._build_system_prompt(context)
        conversation = [{"role": "user", "content": message}]
        
        # Execution Loop
        max_turns = 5
        for _ in range(max_turns):
            
            response = bedrock_runtime.invoke_model(
                modelId=self.bedrock_model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2000,
                    "temperature": 0.5,
                    "system": system_prompt,
                    "messages": conversation,
                    "tools": self.tools
                })
            )
            
            response_body = json.loads(response['body'].read())
            message_content = response_body['content']
            
            assistant_message = {"role": "assistant", "content": message_content}
            conversation.append(assistant_message)
            
            stop_reason = response_body.get('stop_reason')
            
            if stop_reason == 'tool_use':
                tool_results = []
                
                for block in message_content:
                    if block['type'] == 'tool_use':
                        tool_id = block['id']
                        tool_name = block['name']
                        tool_input = block['input']
                        
                        logger.info(f"Executing tool: {tool_name} with input: {tool_input}")
                        result_content = self._execute_tool(tool_name, tool_input)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": str(result_content)
                        })
                
                conversation.append({
                    "role": "user",
                    "content": tool_results
                })
                continue
            
            else:
                final_text = ""
                for block in message_content:
                    if block['type'] == 'text':
                        final_text += block['text']
                return final_text
        
        return "Error: Maximum conversation turns exceeded."

    def _chat_openai(self, message: str, context: Dict[str, Any] = None) -> str:
        if not self.openai_api_key:
            return "AI Configuration Error: OpenAI API Key not configured."

        from openai import OpenAI
        client = OpenAI(api_key=self.openai_api_key)
        
        system_prompt = self._build_system_prompt(context)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Transform tools to OpenAI format
        openai_tools = []
        for tool in self.tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"]
                }
            })

        max_turns = 5
        for _ in range(max_turns):
            response = client.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            messages.append(response_message)
            
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    logger.info(f"Executing tool: {function_name} with input: {function_args}")
                    function_response = self._execute_tool(function_name, function_args)
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(function_response),
                    })
            else:
                return response_message.content

        return "Error: Maximum conversation turns exceeded."

    def _chat_gemini(self, message: str, context: Dict[str, Any] = None) -> str:
         if not self.gemini_api_key:
            return "AI Configuration Error: Gemini API Key not configured."
         
         # Note: Full tool use implementation for Gemini would go here. 
         # For brevity, implementing basic chat for this iteration.
         import google.generativeai as genai
         
         genai.configure(api_key=self.gemini_api_key)
         model = genai.GenerativeModel(self.gemini_model)
         
         system_prompt = self._build_system_prompt(context)
         full_prompt = f"System: {system_prompt}\nUser: {message}"
         
         response = model.generate_content(full_prompt)
         return response.text

    def _execute_tool(self, name, args):
        try:
            if name == "create_host":
                return zabbix_service.create_host(
                    host_name=args['host_name'],
                    ip_address=args['ip_address'],
                    group_id=args['group_id'],
                    template_ids=args.get('template_ids'),
                    description=args.get('description', ''),
                    interface_type=args.get('interface_type', 1),
                    port=args.get('port', '10050')
                )
            elif name == "get_templates":
                return zabbix_service.get_templates(search=args.get('search'))
            elif name == "get_host_groups":
                return zabbix_service.get_groups()
            elif name == "acknowledge_problem":
                return zabbix_service.acknowledge_problem(
                    args['event_id'], args['message']
                )
            elif name == "schedule_maintenance":
                return zabbix_service.schedule_maintenance(
                    args['host_id'], args['minutes'], args.get('description', 'AI Agent Maintenance')
                )
            elif name == "update_host_status":
                return zabbix_service.update_host_status(
                    args['host_id'], args['status']
                )
            else:
                return f"Unknown tool: {name}"
        except Exception as e:
            return f"Tool Execution Error: {str(e)}"

    def _build_system_prompt(self, context):
        base_prompt = """You are a Senior Site Reliability Engineer (SRE) and Zabbix Expert AI Agent.
Your goal is to Help the user manage their infrastructure proactively and intelligently.

### PROTOCOLO DE CREACIÓN DE HOST (Cuando el usuario pide crear un host):
NO uses la herramienta `create_host` inmediatamente. Debes actuar como un ingeniero experto y entrevistar al usuario para configurar el host PERFECTAMENTE.
Sigue estos pasos OBLIGATORIOS:

1.  **Preguntar Sistema Operativo / Plataforma**: (Linux, Windows, Docker, Cisco...) para saber qué Templates son necesarios.
2.  **Preguntar Método de Conexión**: Si no se especifica, preguntar si usar Agente Zabbix, SNMP, JMX o IPMI.
3.  **Sugerir/Buscar Templates**: Usa la herramienta `get_templates` para buscar templates recomendados basados en su respuesta (ej. "Linux by Zabbix agent", "Windows by Zabbix agent").
4.  **Confirmar Configuración**: Antes de ejecutar, resume: "Crearé host X con IP Y, usando template Z y conexión W. ¿Procedo?"

SOLO cuando tengas toda esta info completa, ejecuta `create_host`.

### RESPONSE STYLE:
- Usa formato Markdown rico (headers, bold, lists).
- Respuestas técnicas y precisas. 
- Si faltan datos críticos, PREGUNTA.

### TOOLS:
- `get_templates`: Úsala proactivamente si el usuario menciona un SO pero no un template específico.
- `create_host`: Úsala solo después de confirmar los detalles.
"""
        
        if context:
            if context.get('active_problems_count'):
                base_prompt += f"\n\nContext: {context.get('active_problems_count')} active problems."
        
        return base_prompt

ai_service = AIService()
