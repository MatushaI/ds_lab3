import timeit
import subprocess

start = timeit.default_timer()

pdf_path = 'Skyteam_Timetable.pdf'
pages1 = '5-307,309-14494'
pages2 = '14495-24770,24772-27514'

subprocess.call("python sub_process.py" + ' ' + pdf_path + ' ' + pages1 + ' skyteam_part1.csv', shell=True)
subprocess.call("python sub_process.py" + ' ' + pdf_path + ' ' + pages2 + ' skyteam_part2.csv', shell=True)


print("The difference of time is :", timeit.default_timer() - start)