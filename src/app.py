"""
SMBFlow - Core Application Module
Lightweight AI Workflow Scheduler for Small Businesses
"""

from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# Storage paths
WORKFLOW_DIR = os.path.join(os.path.dirname(__file__), '..', 'workflows')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Ensure directories exist
os.makedirs(WORKFLOW_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory workflow storage (for MVP)
workflows = {}
executions = []

class Workflow:
    """Workflow model"""
    def __init__(self, id, name, description, steps, trigger):
        self.id = id
        self.name = name
        self.description = description
        self.steps = steps
        self.trigger = trigger
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'trigger': self.trigger,
            'created_at': self.created_at
        }


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'smbflow'})


@app.route('/api/workflows', methods=['GET'])
def list_workflows():
    """List all workflows"""
    return jsonify({
        'workflows': [w.to_dict() for w in workflows.values()]
    })


@app.route('/api/workflows', methods=['POST'])
def create_workflow():
    """Create a new workflow"""
    data = request.json
    
    workflow_id = data.get('id') or f"wf_{len(workflows) + 1}"
    workflow = Workflow(
        id=workflow_id,
        name=data.get('name', 'Untitled Workflow'),
        description=data.get('description', ''),
        steps=data.get('steps', []),
        trigger=data.get('trigger', {})
    )
    
    workflows[workflow_id] = workflow
    
    return jsonify({
        'success': True,
        'workflow': workflow.to_dict()
    }), 201


@app.route('/api/workflows/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get a specific workflow"""
    workflow = workflows.get(workflow_id)
    if not workflow:
        return jsonify({'error': 'Workflow not found'}), 404
    
    return jsonify(workflow.to_dict())


@app.route('/api/workflows/<workflow_id>/run', methods=['POST'])
def run_workflow(workflow_id):
    """Execute a workflow"""
    workflow = workflows.get(workflow_id)
    if not workflow:
        return jsonify({'error': 'Workflow not found'}), 404
    
    # Create execution record
    execution = {
        'id': f"exec_{len(executions) + 1}",
        'workflow_id': workflow_id,
        'status': 'running',
        'started_at': datetime.now().isoformat(),
        'steps_completed': []
    }
    
    # Execute each step (simulated for MVP)
    for i, step in enumerate(workflow.steps):
        execution['steps_completed'].append({
            'step': i + 1,
            'action': step.get('action', 'unknown'),
            'status': 'success'
        })
    
    execution['status'] = 'completed'
    execution['completed_at'] = datetime.now().isoformat()
    executions.append(execution)
    
    return jsonify({
        'success': True,
        'execution': execution
    })


@app.route('/api/executions', methods=['GET'])
def list_executions():
    """List workflow execution history"""
    return jsonify({'executions': executions})


# ==================== TEMPLATES ====================

def load_templates():
    """Load pre-built workflow templates"""
    templates = [
        {
            'id': 'client_onboarding',
            'name': 'Client Onboarding',
            'description': 'Automated welcome sequence for new clients',
            'trigger': {'type': 'webhook', 'event': 'new_client'},
            'steps': [
                {'action': 'send_welcome_email', 'delay': 0},
                {'action': 'create_client_record', 'delay': 0},
                {'action': 'send_onboarding_checklist', 'delay': 3600},
                {'action': 'schedule_follow_up', 'delay': 86400}
            ]
        },
        {
            'id': 'invoice_followup',
            'name': 'Invoice Follow-up',
            'description': 'Automatic payment reminder workflow',
            'trigger': {'type': 'schedule', 'cron': '0 9 * * *'},
            'steps': [
                {'action': 'check_overdue_invoices', 'delay': 0},
                {'action': 'send_reminder_email', 'delay': 0},
                {'action': 'escalate_if_overdue', 'delay': 172800}
            ]
        },
        {
            'id': 'weekly_report',
            'name': 'Weekly KPI Report',
            'description': 'Auto-generate and send weekly reports',
            'trigger': {'type': 'schedule', 'cron': '0 18 * * 5'},
            'steps': [
                {'action': 'aggregate_data', 'delay': 0},
                {'action': 'generate_report', 'delay': 0},
                {'action': 'send_report', 'delay': 0}
            ]
        },
        {
            'id': 'lead_nurture',
            'name': 'Lead Nurture',
            'description': 'Follow-up sequence for new leads',
            'trigger': {'type': 'webhook', 'event': 'new_lead'},
            'steps': [
                {'action': 'add_to_crm', 'delay': 0},
                {'action': 'send_intro_email', 'delay': 300},
                {'action': 'add_to_nurture_sequence', 'delay': 3600}
            ]
        },
        {
            'id': 'support_triage',
            'name': 'Support Ticket Triage',
            'description': 'Auto-categorize and route support requests',
            'trigger': {'type': 'webhook', 'event': 'new_ticket'},
            'steps': [
                {'action': 'categorize_ticket', 'delay': 0},
                {'action': 'route_to_team', 'delay': 0},
                {'action': 'send_acknowledgment', 'delay': 0}
            ]
        }
    ]
    
    # Create workflow objects from templates
    for t in templates:
        workflow = Workflow(
            id=t['id'],
            name=t['name'],
            description=t['description'],
            steps=t['steps'],
            trigger=t['trigger']
        )
        workflows[t['id']] = workflow
    
    return templates


# Initialize templates on startup
load_templates()


if __name__ == '__main__':
    print("🚀 SMBFlow - Starting server...")
    print(f"   Default workflows loaded: {len(workflows)}")
    app.run(host='0.0.0.0', port=5000, debug=True)