## Configuración de Amazon Bedrock con API Key

### Paso 1: Generar tu API Key de Bedrock

1. Ve a **AWS Console** → **Amazon Bedrock**
2. En el menú lateral, selecciona **API keys**
3. Haz clic en **Generate API key**
4. Elige el tipo:
   - **Short-term** (recomendado): válida por 12 horas, más segura
   - **Long-term**: válida de 1 día a 1 año
5. **Copia la API key inmediatamente** (empieza con `ABS...`)
   - ⚠️ No podrás verla de nuevo después de cerrar el diálogo

### Paso 2: Configurar el archivo .env

```bash
cd /home/ubuntu/zabbix_agent/backend
cp .env.example .env
nano .env
```

Edita el archivo `.env` y pega tu API key:

```bash
# Amazon Bedrock API Key (empieza con ABS)
BEDROCK_API_KEY=ABS1234567890abcdefghijklmnopqrstuvwxyz...
AWS_REGION=us-east-1

# Zabbix Configuration (ya configuradas)
ZABBIX_URL=http://localhost/zabbix
ZABBIX_USER=Admin
ZABBIX_PASSWORD=zabbix
```

### Paso 3: Habilitar el modelo Claude en Bedrock

Antes de usar el modelo debes habilitarlo:

1. **AWS Console** → **Amazon Bedrock**
2. En el menú lateral: **Model access**
3. Haz clic en **Modify model access** (o **Request model access**)
4. Busca y selecciona: **Anthropic Claude 3.5 Sonnet V2**
5. Haz clic en **Save changes** o **Submit**
6. Espera a que el estado cambie a **Access granted** (puede tomar unos minutos)

### Paso 4: Reiniciar el backend

```bash
cd /home/ubuntu/zabbix_agent
pkill -f "python.*main.py"
bash start_backend.sh
```

### Verificación

Abre el chat flotante en Zabbix y envía un mensaje. Si todo está configurado correctamente, Claude responderá.

### Solución de problemas

**Error: "BEDROCK_API_KEY not configured"**
- Verifica que el archivo `.env` existe en `/home/ubuntu/zabbix_agent/backend/`
- Asegúrate de que la línea no tiene espacios extras: `BEDROCK_API_KEY=ABS...`

**Error: "AccessDeniedException"**
- Ve a **Bedrock > Model access** y verifica que Claude 3.5 Sonnet V2 está habilitado
- Pueden pasar 1-2 minutos después de solicitar acceso

**Error: "ExpiredToken"**
- Tu API key de corto plazo expiró (12 horas)
- Genera una nueva API key desde la consola de Bedrock

### Tipos de API Keys

- **Short-term (Recomendada)**: 
  - Válida hasta 12 horas
  - Más segura, se auto-refresca
  - Ideal para producción

- **Long-term**: 
  - Válida de 1 día a 1 año (o sin expiración)
  - Más fácil para desarrollo
  - Requiere rotación manual
  - AWS recomienda NO usarlas en producción

### Modelo configurado

- **ID**: `us.anthropic.claude-3-5-sonnet-20241022-v2:0`
- **Región**: `us-east-1` (configurable en .env)
- **Contexto**: El modelo tiene acceso a los problemas activos de Zabbix
- **Idioma**: Puede responder en español o inglés según el contexto
