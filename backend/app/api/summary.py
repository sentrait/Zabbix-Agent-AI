from fastapi import APIRouter
from ..services.ai_service import ai_service
from ..services.zabbix_service import zabbix_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/summary/daily")
async def get_daily_summary():
    """Generate a daily AI summary for dashboard widget"""
    try:
        # Gather Zabbix data
        problems = zabbix_service.get_problems()
        hosts = zabbix_service.get_hosts()
        
        # Count severities
        critical_count = sum(1 for p in problems if str(p.get('severity', '0')) in ['4', '5'])
        high_count = sum(1 for p in problems if str(p.get('severity', '0')) == '3')
        
        # Identify critical issues
        critical_issues = []
        for problem in problems[:5]:
            severity = str(problem.get('severity', '0'))
            if severity in ['3', '4', '5']:
                critical_issues.append({
                    'name': problem.get('name', 'Unknown'),
                    'severity': severity,
                    'description': f"Duración: {problem.get('age', 'Unknown')}"
                })
        
        # Ask AI for insights
        context_message = f"""Genera un breve análisis (2-3 oraciones) del estado actual de la infraestructura.

Datos actuales:
- Total hosts: {len(hosts)}
- Problemas activos: {len(problems)}
- Problemas críticos: {critical_count}
- Problemas importantes: {high_count}

Problemas principales: {', '.join([p.get('name', '') for p in problems[:3]])}

Proporciona solo el análisis, sin encabezados ni formato."""
        
        ai_insights = ai_service.chat(context_message, {})
        
        # Build summary response
        status_label = "🟢 SALUDABLE"
        status_color = "#dcfce7"
        status_border = "#10b981"
        
        if critical_count > 0:
            status_label = "🔴 CRÍTICO"
            status_color = "#fee2e2"
            status_border = "#ef4444"
        elif high_count > 0 or len(problems) > 3:
            status_label = "🟡 PRECAUCIÓN"
            status_color = "#fef3c7"
            status_border = "#f59e0b"
        
        summary = {
            "title": "Resumen Diario de IA",
            "overall_status": {
                "label": status_label,
                "description": f"{len(problems)} problema(s) activo(s)",
                "color": status_color,
                "border_color": status_border
            },
            "stats": [
                {"label": "Hosts Monitoreados", "value": str(len(hosts)), "color": "#3b82f6"},
                {"label": "Problemas Activos", "value": str(len(problems)), "color": "#f59e0b"},
                {"label": "Críticos", "value": str(critical_count), "color": "#ef4444"}
            ],
            "critical_issues": critical_issues[:3],
            "recommendations": [
                "Revisar problemas críticos de inmediato" if critical_count > 0 else "Mantener monitoreo preventivo",
                "Actualizar Zabbix server si está desactualizado",
                "Revisar espacio en disco de servidores principales"
            ],
            "insights": ai_insights
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"Error generating daily summary: {e}")
        return {"error": str(e)}
