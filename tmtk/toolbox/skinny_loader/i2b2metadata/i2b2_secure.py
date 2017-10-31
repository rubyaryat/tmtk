from ..generic import TableRow, Defaults, calc_hlevel, get_concept_identifier

import pandas as pd


class I2B2Secure(TableRow):

    def __init__(self, study):

        self.study = study
        super().__init__()

        row_list = [self.build_variable_row(var) for var in study.Clinical.filtered_variables.values()]
        row_list += [*self.add_top_nodes()]

        self.df = pd.DataFrame(row_list, columns=self.columns)

    def add_missing_folders(self):
        """ Add rows for all parent folders not present yet. """
        self.df.apply(lambda x: self._add_folders(x.c_fullname), axis=1)

    def _add_folders(self, path):
        parent = path.rsplit('\\', 2)[0] + '\\'
        if parent == '\\':
            return
        if not any(self.df.c_fullname == parent):
            self.add_folder_row(parent)
        self._add_folders(parent)

    def build_variable_row(self, var):

        row = self.row

        row.c_fullname = '{}\\{}\\'.format(self.study.top_node, var.concept_path)
        row.c_hlevel = calc_hlevel(row.c_fullname)
        row.c_name = var.data_label
        row.c_visualattributes = var.visual_attributes
        row.c_basecode = get_concept_identifier(var, self.study)
        row.c_dimcode = row.c_fullname

        return row

    def back_populate_ontology(self, concept_dimension):
        for concept_row in concept_dimension.df.itertuples():
            concept_code = concept_row[1]
            concept_path = concept_row[2]
            concept_name = concept_row[3]
            row = self.df[self.df.c_basecode == concept_code].copy()
            row.c_fullname = concept_path
            row.c_hlevel = calc_hlevel(concept_path)
            row.c_name = concept_name
            self.df = self.df.append(row, ignore_index=True, verify_integrity=False)

    def add_top_nodes(self):
        """
        Generate add study node itself and any preceding nodes as 'CA' containers.
        """

        row = self.row

        row.c_fullname = self.study.top_node + '\\'
        row.c_hlevel = calc_hlevel(row.c_fullname)
        row.c_visualattributes = 'FAS'
        row.c_facttablecolumn = '@'
        row.c_tablename = 'STUDY'
        row.c_columnname = 'STUDY_ID'
        row.c_operator = 'T'
        row.c_name = self.study.study_name
        row.c_synonym_cd = 'N'
        row.c_columndatatype = 'T'
        row.c_dimcode = row.c_fullname

        yield row

        parent_nodes = row.c_fullname.strip(Defaults.DELIMITER).split(Defaults.DELIMITER)
        path = Defaults.DELIMITER
        for i, parent in enumerate(parent_nodes[:-1]):
            row = row.copy()
            path = '{}{}{}'.format(path, parent, Defaults.DELIMITER)
            row.c_fullname = path
            row.c_name = parent
            row.c_hlevel = i
            row.c_visualattributes = 'CA'
            row.c_tablename = '@'
            row.c_columnname = '@'
            row.secure_obj_token = None
            row.sourcesystem_cd = None

            yield row

    def add_folder_row(self, path):
        row = self.row
        row.c_fullname = path
        row.c_hlevel = calc_hlevel(path)
        row.c_name = path.strip(Defaults.DELIMITER).split(Defaults.DELIMITER)[-1]
        self.df = self.df.append(row, ignore_index=True, verify_integrity=False)

    @property
    def _row_definition(self):
        return pd.Series(
            data=[
                None,                   # c_hlevel
                None,                   # c_fullname
                None,                   # c_name
                'N',                    # c_synonym_cd
                'FA',                   # c_visualattributes
                None,                   # c_totalnum
                None,                   # c_basecode
                None,                   # c_metadataxml
                'CONCEPT_CD',           # c_facttablecolumn
                'CONCEPT_DIMENSION',    # c_tablename
                'CONCEPT_PATH',         # c_columnname
                'T',                    # c_columndatatype
                'LIKE',                 # c_operator
                None,                   # c_dimcode
                None,                   # c_comment
                None,                   # c_tooltip
                '@',                    # m_applied_path
                None,                   # update_date
                None,                   # download_date
                None,                   # import_date
                self.study.study_id,    # sourcesystem_cd
                None,                   # valuetype_cd
                None,                   # m_exclusion_cd
                None,                   # c_path
                None,                   # c_symbol
                None,                   # i2b2_id
                self.study.study_id],   # secure_obj_token
            index=[
                'c_hlevel',
                'c_fullname',
                'c_name',
                'c_synonym_cd',
                'c_visualattributes',
                'c_totalnum',
                'c_basecode',
                'c_metadataxml',
                'c_facttablecolumn',
                'c_tablename',
                'c_columnname',
                'c_columndatatype',
                'c_operator',
                'c_dimcode',
                'c_comment',
                'c_tooltip',
                'm_applied_path',
                'update_date',
                'download_date',
                'import_date',
                'sourcesystem_cd',
                'valuetype_cd',
                'm_exclusion_cd',
                'c_path',
                'c_symbol',
                'i2b2_id',
                'secure_obj_token'])
