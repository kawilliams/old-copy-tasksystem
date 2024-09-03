from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskselection.models import Task
import sys
from os import path
import csv

User = get_user_model()

EXPORT_FIELDS = [
  ('code', '2.5em'),
  ('desc', '8em'),
  ('location', '5em'),
  ('starttime', '5em'),
  ('endtime', '5em'),
  ('firstname', '6em'),
  ('lastname', '6em'),
  ('sign-in', '7em'),
  ('sign-out', '7em'),
]

PREAMBLE = """
\\documentclass[12pt]{article}

\\nofiles

\\usepackage[landscape,margin=0.5in]{geometry}
\\usepackage{longtable}

\\begin{document}

\\section*{%s}

\\renewcommand\\arraystretch{2.1}
\\begin{center}
\\begin{longtable}{%s}
\\hline
%s \\\\
\\hline
\\endhead
"""

POSTAMBLE = """
\\hline
\\end{longtable}
\\end{center}
\\end{document}
"""

def sanitize_latex(s):
  return s.replace("&", "\\&")

def format_head(date, fields):
  frmt = "|" + "|".join(["p{" + f[1] + "}" for f in fields]) + "|"
  flds = ["\\textbf{%s}" % (f[0]) for f in fields]
  flds = " & ".join(flds)
  return PREAMBLE % (str(date), frmt, flds)

def format_line(task):
  row = [task.code, task.desc, task.location, 
         task.starttime.strftime("%H:%M"), task.endtime.strftime("%H:%M")]
  if task.sv:
    row = row + [task.sv.first_name, task.sv.last_name]
  else:
    row = row + ["", ""]
  row = row + ["", ""] # sign in/out fields
  row = [str(f) for f in row]
  row = [sanitize_latex(f) for f in row]
  return " & ".join(row) + " \\\\"

class Command(BaseCommand):
  help = 'Prints the signin forms for each day'

  def add_arguments(self, parser):
    parser.add_argument('export_dir', type=str)

  def handle(self, *args, **options):
    task_dates = Task.objects.order_by('date').values('date').distinct()
    for td in task_dates:
      d = td['date'] # FIXME: messy
      tasks = Task.objects.filter(date=d).order_by('starttime', 'code')
      print(d.strftime("%m-%d"))
      texfile = path.join(options['export_dir'], d.strftime("%m-%d") + ".tex")
      # print a tex file with a table for each day
      with open(texfile, "w") as output:
        print(format_head(d, EXPORT_FIELDS), file=output)
        for task in tasks:
          print(format_line(task), file=output)
          print("\\hline", file=output)
        print(POSTAMBLE, file=output)


