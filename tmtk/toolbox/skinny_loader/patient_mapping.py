
class PatientMapping:

    def __init__(self):
        pass

    @property
    def columns(self):
        return ['patient_ide',
                'patient_ide_source',
                'patient_num',
                'patient_ide_status',
                'upload_date',
                'update_date',
                'download_date',
                'import_date',
                'sourcesystem_cd',
                'upload_id',
                ]
