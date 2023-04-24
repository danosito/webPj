import subprocess

def test(inputs):
    tester = inputs[-1]
    inputs = inputs[:-1]
    process = subprocess.Popen(['python', 'solution.py', 'ls', '-l'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for input_data in inputs:
        process.stdin.write(input_data)
    process.stdin.close()
    a = process.stdout.read()
    return tester, a.decode("UTF-8"), inputs