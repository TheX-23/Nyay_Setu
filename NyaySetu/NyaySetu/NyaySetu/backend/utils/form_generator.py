from typing import Dict, Any, List
import json
from datetime import datetime

class LegalFormGenerator:
    """Advanced legal form generator with multiple form types"""
    
    def __init__(self):
        self.form_templates = {
            'FIR': {
                'title': 'First Information Report',
                'sections': [
                    'complainant_details',
                    'incident_details',
                    'accused_details',
                    'witness_details',
                    'evidence_details'
                ]
            },
            'RTI': {
                'title': 'Right to Information Application',
                'sections': [
                    'applicant_details',
                    'information_requested',
                    'public_authority',
                    'grounds_for_request'
                ]
            },
            'COMPLAINT': {
                'title': 'General Complaint Form',
                'sections': [
                    'complainant_details',
                    'complaint_details',
                    'relief_sought',
                    'supporting_documents'
                ]
            },
            'APPEAL': {
                'title': 'Legal Appeal Application',
                'sections': [
                    'appellant_details',
                    'original_order_details',
                    'grounds_for_appeal',
                    'relief_sought'
                ]
            }
        }
        
        self.section_templates = {
            'complainant_details': {
                'name': 'Full Name',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'id_proof': 'ID Proof Type and Number'
            },
            'incident_details': {
                'date_time': 'Date and Time of Incident',
                'location': 'Location of Incident',
                'description': 'Detailed Description of Incident',
                'loss_damage': 'Loss or Damage Suffered'
            },
            'accused_details': {
                'name': 'Name of Accused',
                'address': 'Address of Accused',
                'description': 'Description of Accused'
            },
            'witness_details': {
                'witness_names': 'Names of Witnesses',
                'witness_addresses': 'Addresses of Witnesses',
                'witness_phones': 'Phone Numbers of Witnesses'
            },
            'evidence_details': {
                'documents': 'Supporting Documents',
                'physical_evidence': 'Physical Evidence',
                'digital_evidence': 'Digital Evidence'
            },
            'applicant_details': {
                'name': 'Full Name',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'citizenship': 'Citizenship'
            },
            'information_requested': {
                'subject': 'Subject of Information',
                'details': 'Detailed Description of Information Required',
                'period': 'Time Period for Information',
                'format': 'Preferred Format of Information'
            },
            'public_authority': {
                'authority_name': 'Name of Public Authority',
                'officer_name': 'Name of Public Information Officer',
                'address': 'Address of Public Authority'
            },
            'grounds_for_request': {
                'reason': 'Reason for Requesting Information',
                'public_interest': 'Public Interest Justification'
            },
            'complaint_details': {
                'subject': 'Subject of Complaint',
                'description': 'Detailed Description of Complaint',
                'date_occurred': 'Date When Issue Occurred',
                'previous_actions': 'Previous Actions Taken'
            },
            'relief_sought': {
                'compensation': 'Compensation Sought',
                'action_required': 'Action Required from Authority',
                'timeframe': 'Expected Timeframe for Resolution'
            },
            'supporting_documents': {
                'documents': 'List of Supporting Documents',
                'photographs': 'Photographs (if any)',
                'correspondence': 'Previous Correspondence'
            },
            'appellant_details': {
                'name': 'Full Name of Appellant',
                'address': 'Complete Address',
                'phone': 'Phone Number',
                'email': 'Email Address',
                'representative': 'Legal Representative (if any)'
            },
            'original_order_details': {
                'order_number': 'Original Order Number',
                'order_date': 'Date of Original Order',
                'issuing_authority': 'Authority that Issued Order',
                'order_summary': 'Summary of Original Order'
            },
            'grounds_for_appeal': {
                'legal_grounds': 'Legal Grounds for Appeal',
                'errors': 'Errors in Original Order',
                'new_evidence': 'New Evidence Available'
            }
        }
    
    def generate_form(self, form_type: str, responses: Dict[str, Any]) -> str:
        """Generate a comprehensive legal form"""
        if form_type not in self.form_templates:
            return f"Error: Unknown form type '{form_type}'"
        
        template = self.form_templates[form_type]
        form_content = []
        
        # Add header
        form_content.append("=" * 80)
        form_content.append(f"{template['title'].center(80)}")
        form_content.append("=" * 80)
        form_content.append(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        form_content.append("")
        
        # Generate sections
        for section in template['sections']:
            if section in self.section_templates:
                form_content.extend(self._generate_section(section, responses))
        
        # Add footer
        form_content.append("")
        form_content.append("=" * 80)
        form_content.append("IMPORTANT NOTES:")
        form_content.append("• This is a computer-generated form for reference purposes")
        form_content.append("• Please verify all information before submission")
        form_content.append("• Consult with a legal professional for final review")
        form_content.append("• Keep copies of all supporting documents")
        form_content.append("=" * 80)
        
        return "\n".join(form_content)
    
    def _generate_section(self, section_name: str, responses: Dict[str, Any]) -> List[str]:
        """Generate content for a specific section"""
        section_content = []
        section_template = self.section_templates[section_name]
        
        # Section header
        section_title = section_name.replace('_', ' ').title()
        section_content.append(f"--- {section_title} ---")
        section_content.append("")
        
        # Generate fields
        for field_key, field_label in section_template.items():
            field_value = responses.get(field_key, '')
            
            if field_value:
                section_content.append(f"{field_label}: {field_value}")
            else:
                section_content.append(f"{field_label}: _________________")
            
            section_content.append("")
        
        return section_content
    
    def get_form_fields(self, form_type: str) -> Dict[str, List[str]]:
        """Get available fields for a specific form type"""
        if form_type not in self.form_templates:
            return {}
        
        fields = {}
        for section in self.form_templates[form_type]['sections']:
            if section in self.section_templates:
                fields[section] = list(self.section_templates[section].keys())
        
        return fields

# Global instance
form_generator = LegalFormGenerator()

def generate_form(form_type: str, responses: Dict[str, Any]) -> str:
    """Main function to generate legal forms"""
    try:
        return form_generator.generate_form(form_type, responses)
    except Exception as e:
        return f"Error generating form: {str(e)}"

def get_form_fields(form_type: str) -> Dict[str, List[str]]:
    """Get available fields for a form type"""
    try:
        return form_generator.get_form_fields(form_type)
    except Exception as e:
        return {}
