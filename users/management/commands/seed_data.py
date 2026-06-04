from django.core.management.base import BaseCommand
from users.models import User, Role,Action, Module, RolePermission



class Command(BaseCommand):
    help = 'Seed initial data: roles, modules, actions, and role permissions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # ---------- Actions ----------
        actions_data = [
            {'name': 'ADD', 'code': 'add'},
            {'name': 'VIEW', 'code': 'view'},
            {'name': 'UPDATE', 'code': 'update'},
            {'name': 'DELETE', 'code': 'delete'},
            {'name': 'EXPORT', 'code': 'export'},
            {'name': 'IMPORT', 'code': 'import'},
            {'name': 'DOWNLOAD', 'code': 'download'},
            {'name': 'CANCEL', 'code': 'cancel'},
            {'name': 'COPY', 'code': 'copy'},
            {'name': 'DRAFT', 'code': 'draft'},
            {'name': 'REJECT', 'code': 'reject'},
        ]
        actions = {}
        for act in actions_data:
            obj, created = Action.objects.get_or_create(code=act['code'], defaults={'name': act['name']})
            actions[act['code']] = obj
            if created:
                self.stdout.write(f'  Created action: {obj.name}')
            else:
                self.stdout.write(f'  Action already exists: {obj.name}')

        # ---------- Modules ----------
        modules_data = [
            {'name': 'Dashboard', 'code': 'dashboard', 'icon': 'file-text', 'order': 1},
            {'name': 'Shipments', 'code': 'shipments', 'icon': 'folder', 'order': 2},
            {'name': 'Customers', 'code': 'customers', 'icon': 'tags', 'order': 3},
            {'name': 'Document Type', 'code': 'document_type', 'icon': 'comments', 'order': 4},
            {'name': 'Equipment', 'code': 'equipment', 'icon': 'image', 'order': 5},
            {'name': 'Equipment Types', 'code': 'equipment_types', 'icon': 'users', 'order': 6},
            {'name': 'Email Templates', 'code': 'email_templates', 'icon': 'shield', 'order': 7},
            {'name': 'Shipper Freight Forwarder Map', 'code': 'shipper_freight_forwarder_map', 'icon': 'cog', 'order': 8},
            {'name': 'User Management', 'code': 'user_management', 'icon': 'file-text', 'order': 9},
            {'name': 'User Roles', 'code': 'user_roles', 'icon': 'folder', 'order': 10},
            {'name': 'Status', 'code': 'status', 'icon': 'tags', 'order': 11},
            {'name': 'Regions', 'code': 'regions', 'icon': 'comments', 'order': 12},
            {'name': 'Sub regions', 'code': 'sub_regions', 'icon': 'image', 'order': 13},
            {'name': 'Countries', 'code': 'countries', 'icon': 'users', 'order': 14},
            {'name': 'Carrier Types', 'code': 'carrier_types', 'icon': 'shield', 'order': 15},
            {'name': 'Transport Modes', 'code': 'transport_modes', 'icon': 'users', 'order': 16},
            {'name': 'User Activity Logs', 'code': 'user_activity_logs', 'icon': 'history', 'order': 17},
        ]
        modules = {}
        for mod in modules_data:
            obj, created = Module.objects.get_or_create(
                code=mod['code'],
                defaults={
                    'name': mod['name'],
                    'icon': mod.get('icon'),
                    'order': mod.get('order', 0)
                }
            )
            modules[mod['code']] = obj
            if created:
                self.stdout.write(f'  Created module: {obj.name}')
            else:
                self.stdout.write(f'  Module already exists: {obj.name}')

        # ---------- Roles ----------
        roles_data = [
            {'name': 'Super Admin', 'code': 'super_admin','description': 'Platform owner / product operations'},
            {'name': 'Port Admin', 'code': 'port_admin','description': 'Port authority customer administrator.'},
            {'name': 'Port User', 'code': 'port_user','description': 'Port operational user handling day-to-day activities.'},
            {'name': 'Shipper', 'code': 'shipper','description': 'Shipment owner who creates shipments before gate entry.'},
            {'name': 'Freight Forwarder', 'code': 'freight_forwarder','description': 'Creates and manages shipments on behalf of shippers.'},
            {'name': 'Consignee', 'code': 'consignee','description': 'The receiver of the goods.'},
            {'name': 'Customs Officer', 'code': 'customs_officer','description': 'Performs inspection and records inspection results.'},
            {'name': 'Customs Supervisor', 'code': 'customs_supervisor','description': 'Reviews inspections, handles escalations and approvals.'},
        ]
        roles = {}
        for role in roles_data:
            obj, created = Role.objects.get_or_create(code=role['code'], defaults={'name': role['name'], 'description': role.get('description')})
            roles[role['code']] = obj
            if created:
                self.stdout.write(f'  Created role: {obj.name}')
            else:
                self.stdout.write(f'  Role already exists: {obj.name}')

        # ---------- Role Permissions ----------
        # Define mapping: role_code -> module_code -> list of action codes
        permissions_map = {
            'super_admin': {
                # all modules, all actions
                'dashboard': ['view', 'add', 'update', 'export', 'import', 'download'],
                'shipments': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'customers': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'document_type': ['view', 'add', 'update', 'delete','export', 'import', 'download'],
                'equipment': ['view', 'add', 'update', 'delete'],
                'equipment_types': ['view', 'add', 'update', 'delete'],
                'email_templates': ['view', 'add', 'update', 'delete'],
                'shipper_freight_forwarder_map': ['view', 'add', 'update', 'delete'],
                'user_management': ['view', 'add', 'update', 'delete'],
                'user_roles': ['view', 'add', 'update', 'delete'],
                'status': ['view', 'add', 'update', 'delete'],
                'regions': ['view', 'add', 'update', 'delete'],
                'sub_regions': ['view', 'add', 'update', 'delete'],
                'countries': ['view', 'add', 'update', 'delete'],
                'carrier_types': ['view', 'add', 'update', 'delete'],
                'transport_modes': ['view', 'add', 'update', 'delete'],
                'user_activity_logs': ['view', 'add', 'update', 'delete'],
            },
            'port_admin': {
                'dashboard': ['view', 'add', 'update', 'export', 'import', 'download'],
                'shipments': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'customers': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'document_type': ['view', 'add', 'update', 'delete','export', 'import', 'download'],
                'equipment': ['view', 'add', 'update', 'delete'],
                'equipment_types': ['view', 'add', 'update', 'delete'],
                'email_templates': ['view', 'add', 'update', 'delete'],
                'shipper_freight_forwarder_map': ['view', 'add', 'update', 'delete'],
                'user_management': ['view', 'add', 'update', 'delete'],
                'user_roles': ['view', 'add', 'update', 'delete'],
                'status': ['view', 'add', 'update', 'delete'],
                'regions': ['view', 'add', 'update', 'delete'],
                'sub_regions': ['view', 'add', 'update', 'delete'],
                'countries': ['view', 'add', 'update', 'delete'],
                'carrier_types': ['view', 'add', 'update', 'delete'],
                'transport_modes': ['view', 'add', 'update', 'delete'],
                'user_activity_logs': ['view', 'add', 'update', 'delete'],
            },
            'port_user': {
                'dashboard': ['view', 'add', 'update', 'export', 'import', 'download'],
                'shipments': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'customers': ['view', 'add', 'update', 'delete','export', 'import', 'download','cancel','copy','draft','reject'],
                'document_type': ['view', 'add', 'update', 'delete','export', 'import', 'download'],
                'equipment': ['view', 'add', 'update', 'delete'],
                'equipment_types': ['view', 'add', 'update', 'delete'],
            },
            'shipper': {},  # no module access
            'freight_forwarder': {},  # no module access
            'consignee': {},  # no module access
            'customs_officer': {},  # no module access
            'customs_supervisor': {},  # no module access
        }

        for role_code, module_perms in permissions_map.items():
            role = roles[role_code]
            for module_code, action_codes in module_perms.items():
                module = modules[module_code]
                for action_code in action_codes:
                    action = actions[action_code]
                    obj, created = RolePermission.objects.get_or_create(
                        role=role,
                        module=module,
                        action=action
                    )
                    if created:
                        self.stdout.write(f'  Perm: {role.name} | {module.name} | {action.name}')
                    # else skip

        self.stdout.write(self.style.SUCCESS('Seed data completed successfully!'))