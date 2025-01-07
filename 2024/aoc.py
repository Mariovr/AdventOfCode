import requests
import re
import secret

# Adapted from @MathisHammel

AOC_COOKIE = secret.cookie # AOC session cookie

headers = {
    'cookie': 'session=' + AOC_COOKIE,
    'User-Agent': 'https://github.com/Mariovr'
}

class AOC:
    def __init__(self, day, year=2024, path=None):
        self.day = day
        self.year = year
        self.path = '/'.join(path.split('/')[:-1]) + '/' if path is not None else ''

        try:
            self._input = open(self.path + 'input' + str(self.day) + '.txt').read()
        except FileNotFoundError:
            self._input = None

        try:
            self._example = open(self.path + 'example'+ str(self.day) + '.txt').read()
        except FileNotFoundError:
            self._example = None

    @property
    def input(self):
        if self._input is None:
            req = requests.get(f'https://adventofcode.com/{self.year}/day/{self.day}/input', headers = headers)

            if req.status_code != 200:
                print(f'Fetching input resulted in error {req.status_code}')
                return

            self._input = req.text
            open(self.path + 'input' + str(self.day) + '.txt', 'w').write(self._input)

        return self._input

    def get_example(self, offset=0):
        if self._example is None or self._example[0] != offset:
            req = requests.get(f'https://adventofcode.com/{self.year}/day/{self.day}', headers = headers)

            self._example = (
                offset,
                re.sub('&lt;', '<', re.sub('&gt;', '>', re.sub('<[^<]+?>', '', req.text.split('<pre><code>')[offset+1].split('</code></pre>')[0])))
            )

            open(self.path + 'example'+ str(self.day) + '.txt', 'w').write(self._example[1] + '\n')

        return self._example[1]
    example = property(get_example)

    def submit(self, part, answer):
        print(f'You are about to submit the follwing answer:')
        print(f'>>>>>>>>>>>>>>>>> {answer}')
        input('Press enter to continue or Ctrl+C to abort.')

        response = requests.post(
            f'https://adventofcode.com/{self.year}/day/{self.day}/answer',
            headers = headers,
            data = {
                'level': str(part),
                'answer': str(answer)
                }
            )

        if 'You gave an answer too recently' in response.text:
            # You will get this if you submitted a wrong answer less than 60s ago.
            t = re.search('You have (.*) left to wait.', response.text)
            print(f'VERDICT : TOO MANY REQUESTS. WAIT {t.group(1)}')
        elif 'not the right answer' in response.text:
            if 'too low' in response.text:
                print('VERDICT : WRONG (TOO LOW)')
            elif 'too high' in response.text:
                print('VERDICT : WRONG (TOO HIGH)')
            else:
                print('VERDICT : WRONG (UNKNOWN)')
        elif 'seem to be solving the right level.' in response.text:
            print('VERDICT : ALREADY SOLVED')
        elif 'right answer' in response.text:
            print('VERDICT : OK !')
        else:
            print('VERDICT: UNKNOWN')
            print(response.text)
