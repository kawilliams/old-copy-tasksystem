from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskselection.models import Task
import sys
from os import path
import csv

User = get_user_model()

EXPORT_FIELDS = [
  ('code', '4em'),
  ('desc', '25em'),
  ('location', '7em'),
  ('date', '5em'),
  ('starttime', '5em'),
  ('endtime', '5em')
]

PREAMBLE = """
\\documentclass[12pt]{article}

\\usepackage[landscape,margin=0.5in]{geometry}
\\usepackage{longtable}

\\begin{document}

"""

SV_SECTION_START = """
\\section*{%s}

\\begin{center}
\\begin{longtable}{%s}
\\hline
%s \\\\
\\hline
\\endhead
"""

SV_SECTION_END = """
\\hline
\\end{longtable}
\\end{center}
"""

POSTAMBLE = """
\\end{document}
"""

def sanitize_latex(s):
  return s.replace("&", "\\&")

def format_head(sv, fields):
  frmt = "|" + "|".join(["p{"+f[1]+"}" for f in fields]) + "|"
  flds = ["\\textbf{%s}" % (f[0]) for f in fields]
  flds = " & ".join(flds)
  name = sv.first_name + ' ' + sv.last_name
  return SV_SECTION_START % (name, frmt, flds)

def format_line(task):
  row = [task.code, task.desc, task.location, task.date, 
         task.starttime.strftime("%H:%M"), task.endtime.strftime("%H:%M")]
  row = [str(f) for f in row]
  row = [sanitize_latex(f) for f in row]
  return " & ".join(row) + " \\\\"

class Command(BaseCommand):
  help = 'Prints the task lists for each SV'

  def add_arguments(self, parser):
    parser.add_argument('file', type=str)

  def handle(self, *args, **options):
    with open(options['file'], 'w') as output:
      print(PREAMBLE, file=output)

      # make a page for each SV
      svs = User.objects.order_by('last_name', 'first_name').all()
      for sv in svs:
        tasks = Task.objects.filter(sv=sv).order_by('date', 'starttime')
        if len(tasks) > 0:
          print_sv_tasks(sv, tasks, output)
          print("\\clearpage", file=output)
      print(POSTAMBLE, file=output)
      
def print_sv_tasks(sv, tasks, output):
  print(format_head(sv, EXPORT_FIELDS), file=output)
  for task in tasks:
    print(format_line(task), file=output)
    print("\\hline", file=output)
  print(SV_SECTION_END, file=output)

