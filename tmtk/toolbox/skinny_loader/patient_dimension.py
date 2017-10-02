
class PatientDimension:

    def __init__(self):
        pass

    @property
    def columns(self):
        return ['patient_num',
                'vital_status_cd',
                'birth_date',
                'death_date',
                'sex_cd',
                'age_in_years_num',
                'language_cd',
                'race_cd',
                'marital_status_cd',
                'religion_cd',
                'zip_cd',
                'statecityzip_path',
                'income_cd',
                'patient_blob',
                'update_date',
                'download_date',
                'import_date',
                'sourcesystem_cd',
                'upload_id',
                ]
