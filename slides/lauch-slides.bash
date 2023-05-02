countertimer=$1
warningtime=$2
warningtime_default=2
countertimer_defaul=1

#pdfpc -w -d {$countertimer:=$countertimer_defaul} -l {$warningtime:=$warningtime_default} main.pdf
#pdfpc -w -d {$countertimer} -l {$warningtime} main.pdf
pdfpc -w -d 1 -l 2 main.pdf
