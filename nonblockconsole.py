import sys
import select

#Just a little nonblocking tokenizer for the console.
#Format:
#    $key:value1:value2:value3
#  becomes
#    {key: [value1, value2, value3]}

class NonBlockConsole:

    input = ""

#

    def get_commands(self):
        #returns key/array dictionary as outlined above
        dictionary = {}
        user_input = self.get_input()
        if user_input == None:
            return

        user_input = user_input.rstrip()
        user_input = user_input.split('$')

        for word in user_input:
            values = word.split(':')
            dictionary[values[0]] = values[1:]

        return dictionary

    def get_input(self):
        user_input = ""
        while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line:
                user_input += line
            else:
                print('eof')
                exit(0)
        if user_input != "" or user_input != None:
            return user_input
