from django.core.management.base import BaseCommand
from users.models import User, Role,Action, Module, RolePermission,ModuleActionAssoc
from django.utils import timezone



class Command(BaseCommand):
    help = 'Seed initial data: roles, modules, actions, and role permissions'
    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        admin_user = User.objects.get(pk=1)
        # ---------- Actions ----------
        actions_data = [
            {'name': 'ADD', 'code': 'add','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'VIEW', 'code': 'view','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'UPDATE', 'code': 'update','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'DELETE', 'code': 'delete','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'EXPORT', 'code': 'export','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'IMPORT', 'code': 'import','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'DOWNLOAD', 'code': 'download','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'CANCEL', 'code': 'cancel','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'COPY', 'code': 'copy','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'DRAFT', 'code': 'draft','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'REJECT', 'code': 'reject','created_by':admin_user,'created_at':timezone.now()},
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
            {'name': 'Dashboard', 'code': 'dashboard', 'icon': 'file-text', 'order': 1,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Shipments', 'code': 'shipments', 'icon': 'folder', 'order': 2,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Customers', 'code': 'customers', 'icon': 'tags', 'order': 3,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Document Type', 'code': 'document_type', 'icon': 'comments', 'order': 4,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Equipment', 'code': 'equipment', 'icon': 'image', 'order': 5,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Equipment Types', 'code': 'equipment_types', 'icon': 'users', 'order': 6,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Email Templates', 'code': 'email_templates', 'icon': 'shield', 'order': 7,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Shipper Freight Forwarder Map', 'code': 'shipper_freight_forwarder_map', 'icon': 'cog', 'order': 8,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'User Management', 'code': 'user_management', 'icon': 'file-text', 'order': 9,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'User Roles', 'code': 'user_roles', 'icon': 'folder', 'order': 10,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Status', 'code': 'status', 'icon': 'tags', 'order': 11,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Regions', 'code': 'regions', 'icon': 'comments', 'order': 12,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Sub regions', 'code': 'sub_regions', 'icon': 'image', 'order': 13,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Countries', 'code': 'countries', 'icon': 'users', 'order': 14,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Carrier Types', 'code': 'carrier_types', 'icon': 'shield', 'order': 15,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Transport Modes', 'code': 'transport_modes', 'icon': 'users', 'order': 16,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'User Activity Logs', 'code': 'user_activity_logs', 'icon': 'history', 'order': 17,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Seaport Management', 'code': 'seaport_management', 'icon': 'anchor', 'order': 18,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Container Management', 'code': 'container_management', 'icon': 'archive', 'order': 19,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Package Management', 'code': 'package_management', 'icon': 'archive', 'order': 20,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Company Management', 'code': 'companies', 'icon': 'archive', 'order': 21,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Customer Document Associations', 'code': 'customer_doc_assoc', 'icon': 'archive', 'order': 22,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Carriers', 'code': 'carriers', 'icon': 'truck', 'order': 23,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Customer LSP Associations', 'code': 'customer_lsp_assoc', 'icon': 'archive', 'order': 24,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Carrier Contacts', 'code': 'carrier_contacts', 'icon': 'address-book', 'order': 25,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Inspection Area', 'code': 'inspection_area', 'icon': 'fa-check', 'order': 26,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Custom Officer', 'code': 'custom_officer', 'icon': 'fa-user-police', 'order': 27,'created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Sub Status', 'code': 'sub_status', 'icon': 'archive', 'order': 28,'created_by':admin_user,'created_at':timezone.now()},
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
            {'name': 'Super Admin', 'code': 'super_admin','description': 'Platform owner / product operations','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Port Admin', 'code': 'port_admin','description': 'Port authority customer administrator.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Port User', 'code': 'port_user','description': 'Port operational user handling day-to-day activities.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Shipper', 'code': 'shipper','description': 'Shipment owner who creates shipments before gate entry.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Freight Forwarder', 'code': 'freight_forwarder','description': 'Creates and manages shipments on behalf of shippers.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Consignee', 'code': 'consignee','description': 'The receiver of the goods.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Customs Officer', 'code': 'customs_officer','description': 'Performs inspection and records inspection results.','created_by':admin_user,'created_at':timezone.now()},
            {'name': 'Customs Supervisor', 'code': 'customs_supervisor','description': 'Reviews inspections, handles escalations and approvals.','created_by':admin_user,'created_at':timezone.now()},
        ]
        roles = {}
        for role in roles_data:
            obj, created = Role.objects.get_or_create(code=role['code'], defaults={'name': role['name'], 'description': role.get('description')})
            roles[role['code']] = obj
            if created:
                self.stdout.write(f'  Created role: {obj.name}')
            else:
                self.stdout.write(f'  Role already exists: {obj.name}')


        # ---------- Module Action Permissions ----------
        module_action_map ={
            # all modules, all actions maps
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
            'seaport_management': ['view', 'add', 'update', 'delete'],
            'container_management': ['view', 'add', 'update', 'delete'],
            'package_management': ['view', 'add', 'update', 'delete'],
            'companies': ['view', 'add', 'update', 'delete'],
            'customer_doc_assoc': ['view', 'add', 'update', 'delete'],
            'carriers': ['view', 'add', 'update', 'delete'],
            'customer_lsp_assoc': ['view', 'add', 'update', 'delete'],
            'carrier_contacts': ['view', 'add', 'update', 'delete'],
            'sub_status': ['view', 'add', 'update', 'delete'],
            'inspection_area': ['view', 'add', 'update', 'delete'],
            'custom_officer': ['view', 'add', 'update', 'delete'],
        }
        module_action_assoc_map = {}
        for module_code, action_codes in module_action_map.items():
            module = modules[module_code]
            for action_code in action_codes:
                action = actions[action_code]
                obj, created = ModuleActionAssoc.objects.get_or_create(
                    module=module,
                    action=action,
                    defaults={
                        "created_by": admin_user,
                        "created_at": timezone.now()
                    }
                )
                module_action_assoc_map[
                    f"{module_code}_{action_code}"
                ] = obj

                if created:
                    self.stdout.write(f'Created ModuleActionAssoc: {module.name} | {action.name}')
                # else skip
            

       

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
                'seaport_management': ['view', 'add', 'update', 'delete'],
                'container_management': ['view', 'add', 'update', 'delete'],
                'package_management': ['view', 'add', 'update', 'delete'],
                'companies': ['view', 'add', 'update', 'delete'],
                'customer_doc_assoc': ['view', 'add', 'update', 'delete'],
                'carriers': ['view', 'add', 'update', 'delete'],
                'customer_lsp_assoc': ['view', 'add', 'update', 'delete'],
                'carrier_contacts': ['view', 'add', 'update', 'delete'],
                'sub_status': ['view', 'add', 'update', 'delete'],
                'inspection_area': ['view', 'add', 'update', 'delete'],
                'custom_officer': ['view', 'add', 'update', 'delete'],
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
                'seaport_management': ['view', 'add', 'update', 'delete'],
                'container_management': ['view', 'add', 'update', 'delete'],
                'package_management': ['view', 'add', 'update', 'delete'],
                'inspection_area': ['view', 'add', 'update', 'delete'],
                'custom_officer': ['view', 'add', 'update', 'delete'],
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
                    module_action_assoc = module_action_assoc_map[
                        f"{module_code}_{action_code}"
                    ]
                    obj, created = RolePermission.objects.update_or_create(
                        role=role,
                        # module=module,
                        # action=action,
                        # module=module_action_assoc.module,
                        # action=module_action_assoc.action,
                        module_action_assoc=module_action_assoc,
                        defaults={
                            # "module_action_assoc": module_action_assoc,
                            "created_by": admin_user,
                            "created_at": timezone.now()
                        }
                    )
                    
                    # Existing record hai lekin module_action_assoc empty hai
                    if not created:

                        fields_to_update = []

                        if obj.module_action_assoc_id != module_action_assoc.id:
                            obj.module_action_assoc = module_action_assoc
                            fields_to_update.append("module_action_assoc")

                        if fields_to_update:
                            obj.save(update_fields=fields_to_update)

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Created: '
                                f'{role.name} | '
                                f'{module_action_assoc.module.name} | '
                                f'{module_action_assoc.action.name}'
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Updated: '
                                f'{role.name} | '
                                f'{module_action_assoc.module.name} | '
                                f'{module_action_assoc.action.name}'
                            )
                        )

                    if created:
                        self.stdout.write(f'  Perm: {role.name} | {module.name} | {action.name}')
                    # else skip

        self.stdout.write(self.style.SUCCESS('Seed data completed successfully!'))
