import subprocess as sp

# p = sp.Popen("powershell -NoLogo -NonInteractive",
#              shell=True, stdout=sp.PIPE, stdin=sp.PIPE)
# lines = p.communicate(b"$(get-process -Name fluent_queue | Group-Object -Property name).count")
# # print(p.stdout.read())
# lines = lines[0].decode()
# print(lines)


def count_application(application_name):
    a = sp.run("powershell -command $(get-process -Name '%s' | Group -Property name).count" % application_name,
               stdout=sp.PIPE, stderr=sp.PIPE).stdout
    return int(a)


number = count_application('fluent_queue')
print(number)

