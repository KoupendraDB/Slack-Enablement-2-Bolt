from datetime import date

def get_create_task_form_from_payload(text, user):
    form = {}
    lines = text.split('\n')
    line_number = 0
    while line_number < len(lines) - 1:
        line = lines[line_number].strip()
        if line == 'Title:':
            line_number += 1
            form['title'] = lines[line_number]
        elif line == 'Description:':
            line_number += 1
            description = []
            new_field = False
            while line_number < len(lines):
                line = lines[line_number].strip()
                if line not in ['Title:', 'Assignee:', 'Due:']:
                    description.append(line + '\n')
                    line_number += 1
                else:
                    new_field = True
                    break
            form['description_type'] = 'mrkdwn'
            form['description'] = ''.join(description)
            if new_field:
                continue
        elif line == 'Assignee:':
            line_number += 1
            if line_number < len(lines):
                line = lines[line_number]
                assignee = line.replace('<', '').replace('>', '').split('|')[0].replace('@', '')
                form['assignee'] = assignee
        elif line == 'Due:':
            line_number += 1
            if line_number < len(lines):
                line = lines[line_number]
                if date.fromisoformat(line):
                    form['eta_done'] = line
        line_number += 1
    
    if not form.get('assignee', False):
        form['assignee'] = user
    
    if not form.get('eta_done', False):
        form['eta_done'] = date.today().isoformat()
    
    if form.get('title', None) and form.get('description', None):
        return form

    return None