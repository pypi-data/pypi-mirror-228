from configparser import ConfigParser
import openai

def config(filename='credentials.ini', section='openai'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    openaiparam = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            openaiparam[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return openaiparam

def main():
    """
    Read the credentials from the credentials.ini file and authenticate with OpenAI.
    """

    params = config()
    api_key = params['openai_api_key']

    openai.api_key = api_key

if __name__ == '__main__':
    main()
