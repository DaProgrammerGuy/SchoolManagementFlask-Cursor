# Paste here the serialize_subject, serialize_grade, serialize_student, serialize_teacher and any other helper functions from DRY.py 

def add_items_to_user(item_type, item_names, object_instance, relationship_attr, model_class, db):
    existing_items = getattr(object_instance, relationship_attr)
    warnings = []
    added = []
    if isinstance(item_names, str):
        item_names = [item_names]
    for name in item_names:
        if isinstance(existing_items, list):
            if any(item.name == name for item in existing_items):
                warnings.append(f"{item_type} {name} already exists for {object_instance.username}")
                continue
        else:
            if existing_items and existing_items.name == name:
                warnings.append(f"{item_type} {name} already exists for {object_instance.username}")
                continue
        item = model_class.query.filter_by(name=name).first()
        if not item:
            item = model_class(name=name)
            db.session.add(item)
            db.session.commit()
        if isinstance(existing_items, list):
            existing_items.append(item)
        else:
            setattr(object_instance, relationship_attr, item)
        added.append(name)
    return warnings, added

def add_items_to_grade(item_type, item_names, object_instance, relationship_attr, model_class, db):
    existing_items = getattr(object_instance, relationship_attr)
    warnings = []
    added = []
    if isinstance(item_names, str):
        item_names = [item_names]
    for name in item_names:
        if isinstance(existing_items, list):
            if any(item.name == name for item in existing_items):
                warnings.append(f"{item_type} {name} already exists for {object_instance.name}")
                continue
        else:
            if existing_items and existing_items.name == name:
                warnings.append(f"{item_type} {name} already exists for {object_instance.name}")
                continue
        item = model_class.query.filter_by(name=name).first()
        if not item:
            item = model_class(name=name)
            db.session.add(item)
            db.session.commit()
        if isinstance(existing_items, list):
            existing_items.append(item)
        else:
            setattr(object_instance, relationship_attr, item)
        added.append(name)
    return warnings, added

def add_items_to_grade2(item_type, item_names, object_instance, relationship_attr, model_class, db):
    existing_items = getattr(object_instance, relationship_attr)
    warnings = []
    added = []
    if isinstance(item_names, str):
        item_names = [item_names]
    for name in item_names:
        if isinstance(existing_items, list):
            if any(item.username == name for item in existing_items):
                warnings.append(f"{item_type} {name} already exists for {object_instance.name}")
                continue
        else:
            if existing_items and existing_items.name == name:
                warnings.append(f"{item_type} {name} already exists for {object_instance.name}")
                continue
        item = model_class.query.filter_by(username=name).first()
        if not item:
            item = model_class(username=name)
            db.session.add(item)
            db.session.commit()
        if isinstance(existing_items, list):
            existing_items.append(item)
        else:
            setattr(object_instance, relationship_attr, item)
        added.append(name)
    return warnings, added

def serialize_grade(item):
    return {
        "id": item.id,
        "name": item.name,
        "subjects": [sub.name for sub in item.subjects],
        "students": [stud.username for stud in item.students],
        "teachers": [teacher.username for teacher in item.teachers]
    }

def serialize_subject(item):
    return {
        "id": item.id,
        "name": item.name,
        "grades": [grade.name for grade in item.grades],
        "students": [student.username for student in item.students],
        "teachers": [teacher.username for teacher in item.teachers]
    }

def serialize_student(item):
    return {
        "id": item.id,
        "username": item.username,
        "grade(s)": item.grade.name,
        "subject(s)": [s.name for s in item.student_subjects]
    }

def serialize_teacher(item):
    return {
        "id": item.id,
        "username": item.username,
        "grade(s)": [g.name for g in item.teacher_grades],
        "Subject(s)": [s.name for s in item.teacher_subjects]
    } 