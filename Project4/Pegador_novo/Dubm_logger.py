class DumbLogger:
    def __init__(self, RECORD_LOG=False):
        self.file_name = 'catcher.html'
        self.isDumb = not RECORD_LOG

    def log(self, str, end = '<br>\n'):
        if not self.isDumb:
            with open(self.file_name, 'a', encoding='utf-8') as file:
                file.write('{}{}'.format(str, end))
                file.write('\n<script>window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);</script>\n')


    def sep(self):
        if not self.isDumb:
            with open(self.file_name, 'a', encoding='utf-8') as file:
                file.write('<br>\n' + '-' * 70 + '<br>\n')
                file.write('\n<script>window.scrollTo(0, document.body.scrollHeight || document.documentElement.scrollHeight);</script>\n')

