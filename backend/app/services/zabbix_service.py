import os
import logging
from pyzabbix import ZabbixAPI
import time

logger = logging.getLogger(__name__)

class ZabbixService:
    def __init__(self):
        # Zabbix API URL
        self.url = os.getenv("ZABBIX_URL", "http://127.0.0.1/zabbix")
        self.user = os.getenv("ZABBIX_USER", "Admin")
        self.password = os.getenv("ZABBIX_PASSWORD", "zabbix")
        self.verify_ssl = os.getenv("ZABBIX_VERIFY_SSL", "False").lower() == "true"
        self.api = None
        logger.info(f"ZabbixService initialized with URL: {self.url}")

    def connect(self):
        if self.api and self.api.auth:
            return
        
        try:
            logger.info(f"Attempting to connect to Zabbix at {self.url}")
            self.api = ZabbixAPI(self.url)
            self.api.session.verify = self.verify_ssl
            self.api.login(self.user, self.password)
            logger.info(f"Successfully connected to Zabbix API")
        except Exception as e:
            logger.error(f"Failed to connect to Zabbix API: {e}")
            raise

    def get_hosts(self):
        self.connect()
        return self.api.host.get(output=["hostid", "host", "name", "status"], selectInterfaces=["ip", "dns"])

    def get_host_items(self, host_id):
        self.connect()
        return self.api.item.get(hostids=host_id, output=["itemid", "name", "key_", "lastvalue", "units"])

    def get_problems(self):
        self.connect()
        return self.api.problem.get(
            output="extend",
            recent=True,
            sortfield=["eventid"],
            sortorder="DESC",
            limit=20
        )

    def get_groups(self):
        self.connect()
        return self.api.hostgroup.get(output=["groupid", "name"])

    def get_templates(self, search=None):
        self.connect()
        params = {"output": ["templateid", "name"]}
        if search:
            params["search"] = {"name": search}
        return self.api.template.get(**params)

    def create_host(self, host_name, ip_address, group_id, template_ids=None, description="", interface_type=1, port="10050", dns=""):
        """
        Create a host with advanced configuration.
        interface_type: 1=Agent, 2=SNMP, 3=IPMI, 4=JMX
        """
        self.connect()
        try:
            # Prepare interface
            interfaces = [{
                "type": int(interface_type),
                "main": 1,
                "useip": 1 if ip_address else 0,
                "ip": ip_address,
                "dns": dns,
                "port": str(port)
            }]
            
            params = {
                "host": host_name,
                "interfaces": interfaces,
                "groups": [{"groupid": group_id}],
                "description": description
            }
            
            if template_ids:
                # Handle single ID or list of IDs
                if isinstance(template_ids, str):
                   template_ids = [template_ids] 
                
                params["templates"] = [{"templateid": tid} for tid in template_ids]
            
            result = self.api.host.create(params)
            logger.info(f"Host created successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to create host: {e}")
            raise Exception(f"Zabbix API Error: {str(e)}")

    def get_history(self, item_id, limit=100):
        self.connect()
        return self.api.history.get(itemids=item_id, sortfield="clock", sortorder="DESC", limit=limit, history=0)
    
    # === NEW AGENTIC METHODS ===

    def get_host_id_by_name(self, name):
        """Helper to find host ID by visible name or hostname"""
        self.connect()
        hosts = self.api.host.get(filter={"name": name}, output=["hostid"])
        if not hosts:
            hosts = self.api.host.get(filter={"host": name}, output=["hostid"])
        
        return hosts[0]['hostid'] if hosts else None

    def get_host_details(self, name_or_ip):
        """Get host details including active problems"""
        self.connect()
        try:
            # Try to find host by name, visible name or interface IP
            hosts = self.api.host.get(
                search={"name": name_or_ip, "host": name_or_ip, "ip": name_or_ip},
                searchByAny=True,
                output=["hostid", "name", "status", "maintenance_status"],
                selectInterfaces=["ip"],
                selectTags="extend"
            )
            
            if not hosts:
                # Fallback: strict filter tag matching often fails fuzzy search, try just list matching
                # But for now, if not found, return message
                return {"found": False, "message": f"Host '{name_or_ip}' not found in Zabbix."}
            
            host = hosts[0]
            host_id = host['hostid']
            
            # Get Active Problems
            problems = self.api.problem.get(
                hostids=host_id,
                output=["eventid", "name", "severity", "clock"],
                recent="true", # Include recently resolved
                sortfield="eventid",
                sortorder="DESC"
            )
            
            # Map severity to text
            severity_map = {
                "0": "Not classified", "1": "Information", "2": "Warning",
                "3": "Average", "4": "High", "5": "Disaster"
            }
            
            active_problems = []
            for p in problems:
                active_problems.append({
                    "name": p['name'],
                    "severity": severity_map.get(p['severity'], "Unknown"),
                    "since": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(p['clock'])))
                })
                
            return {
                "found": True,
                "name": host['name'],
                "status": "Monitored" if host['status'] == '0' else "Not Monitored",
                "maintenance": bool(int(host['maintenance_status'])),
                "active_problems_count": len(problems),
                "problems": active_problems
            }
            
        except Exception as e:
            logger.error(f"Error getting host details: {e}")
            return {"error": str(e)}

    def get_problem_id_by_name(self, name):
        """Helper to find a recent problem event ID by name"""
        self.connect()
        problems = self.api.problem.get(search={"name": name}, output=["eventid"], limit=1, recent=True)
        return problems[0]['eventid'] if problems else None

    def acknowledge_problem(self, event_id, message, action_close=False):
        """Acknowledge a problem event"""
        self.connect()
        try:
            if isinstance(event_id, str) and not event_id.isdigit():
                # Try to resolve ID from name if string passed
                resolved_id = self.get_problem_id_by_name(event_id)
                if not resolved_id:
                    raise Exception(f"Could not find problem with name: {event_id}")
                event_id = resolved_id

            action_val = 6 # Default: Acknowledge + Comment
            if action_close:
                action_val |= 1 # Close problem bit

            result = self.api.event.acknowledge(
                eventids=event_id,
                action=action_val,
                message=message
            )
            logger.info(f"Problem acknowledged successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to acknowledge problem: {e}")
            raise Exception(f"Zabbix API Error: {str(e)}")

    def schedule_maintenance(self, host_id, minutes, description="AI Maintenance"):
        """Schedule a one-time maintenance window starting now"""
        self.connect()
        try:
            if isinstance(host_id, str) and not host_id.isdigit():
                resolved_id = self.get_host_id_by_name(host_id)
                if not resolved_id:
                    raise Exception(f"Could not find host with name: {host_id}")
                host_id = resolved_id

            now = int(time.time())
            end = now + (minutes * 60)
            
            params = {
                "name": f"AI Maintenance: {description}",
                "active_since": now,
                "active_till": end,
                "hostids": [host_id],
                "timeperiods": [{
                    "timeperiod_type": 0, # One time only
                    "start_date": now,
                    "period": minutes * 60 # Duration in seconds
                }]
            }
            
            result = self.api.maintenance.create(params)
            logger.info(f"Maintenance scheduled successfully: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to schedule maintenance: {e}")
            raise Exception(f"Zabbix API Error: {str(e)}")

    def update_host_status(self, host_id, status_code):
        """Update host status (0=Monitored/Enabled, 1=Unmonitored/Disabled)"""
        self.connect()
        try:
            if isinstance(host_id, str) and not host_id.isdigit():
                resolved_id = self.get_host_id_by_name(host_id)
                if not resolved_id:
                    raise Exception(f"Could not find host with name: {host_id}")
                host_id = resolved_id

            # Zabbix API expects integer for status
            # 0 = Monitored
            # 1 = Unmonitored
            result = self.api.host.update({
                "hostid": host_id,
                "status": int(status_code)
            })
            logger.info(f"Host status updated successfully to {status_code}: {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to update host status: {e}")
            raise Exception(f"Zabbix API Error: {str(e)}")

zabbix_service = ZabbixService()
