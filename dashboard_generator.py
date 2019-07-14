import os
import os.path
from jinja2 import Environment, FileSystemLoader
from tempfile import NamedTemporaryFile
import yaml
import re
import sys

class DashboardGenerator(object):
    def __init__(self, parent_name, child_name, folder_id, input_template, substitution_file=None):
        self.input_template = input_template
        self.substitution_file = substitution_file
        self.parent_name = parent_name
        self.child_name = child_name
        self.folder_id = folder_id
        self.curdir = os.getcwd()

    def __generate_substitutions(self):
        file = os.path.join(os.path.join(self.curdir,'substitutions/{0}'.format(self.parent_name)),self.substitution_file)
        fd = open(file, 'r')
        substitutions = yaml.load(fd)['substitutions']
        new_dct = dict()
        for tmp_dct in substitutions:
            for key, val in tmp_dct.items():
                new_dct[key] = val
        return new_dct

    def __generate_dashboard_content(self, type):

        jenv = Environment(loader=FileSystemLoader(os.path.join(self.curdir,'templates/{0}'.format(self.parent_name))), trim_blocks=True, extensions=['jinja2.ext.do'])

        if type == 'cloudwatch':
            content = None
            if self.substitution_file:
                substitutions = self.__generate_substitutions()
                substitutions['parent_name'] = self.parent_name
                substitutions['folder_id'] = self.folder_id
                substitutions['child_name'] = self.child_name
                content = jenv.get_template(self.input_template).render(substitutions)
            else:
                content = jenv.get_template(self.input_template).render()
            return content
        elif type == 'graphite':
            content = None
            if self.substitution_file:
                substitutions = self.__generate_substitutions()
                content = jenv.get_template(self.input_template).render(substitutions)
            else:
                content = jenv.get_template(self.input_template).render()
            return content
        else:
            pass


    def __write_to_output_file(self, content, output_file):
        outputdir = os.path.join(self.curdir, 'outputs/{0}'.format(self.parent_name))
        if not output_file:
            outfile = NamedTemporaryFile(mode='w+', suffix='.json', prefix='{0}_{1}_'.format(self.parent_name, self.input_template.split('.')[0]), dir=outputdir, delete=False)
        else:
            outfile = open(os.path.join(outputdir, output_file), 'w+')
        outfile.write(content)

        return os.path.basename(outfile.name)


    def generate_output_file(self, type='cloudwatch', output_file=None):
        contents = self.__generate_dashboard_content(type)
        outfiles = list()
        if isinstance(contents, list):
            for content in contents:
                outfile_name = self.__write_to_output_file(content, output_file)
                outfiles.append(outfile_name)
        else:
            outfile_name = self.__write_to_output_file(contents, output_file)
            outfiles.append(outfile_name)

        return outfiles

if __name__ == '__main__':
    parent_name = sys.argv[1]
    child_name = sys.argv[2]
    folder_id = sys.argv[3]

    '''
    for j2_template in ['dashboard_cloudwatch_ec2.j2', 'dashboard_cloudwatch_elb.j2', 'dashboard_cloudwatch_asg.j2', 'dashboard_cloudwatch_ecs_cluster_standard.j2', 'dashboard_cloudwatch_ecs_service_standard.j2']:
        dashboard_generator = DashboardGenerator(parent_name, child_name, folder_id, j2_template, 'cloudwatch-{0}.yaml'.format(child_name))
        dashboard_generator.generate_output_file() 
    '''
    dashboard_generator = DashboardGenerator(parent_name, child_name, folder_id, 'dashboard_graphite_pgsql.j2', 'graphite-{0}.yaml'.format(child_name))
    dashboard_generator.generate_output_file()
