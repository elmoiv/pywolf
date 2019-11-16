import re, os
from urllib.request import urlopen, urlretrieve

# Main Headers
Headers = {
            1:(
                'Indefinite+integral',
                'IndefiniteIntegral',
                'IndefiniteIntegral__Step-by-step+solution'
                ),
            2:(
                'Definite+integral',
                'Input',
                'Input__Step-by-step+solution'
                ),
            3:(
                'Derivative',
                'Input',
                'Input__Step-by-step+solution'
                )
            }

appid = '3H4296-5YPAGQUJK7'

# URL format ready
URL = 'http://api.wolframalpha.com/v2/query.jsp?appid={}&input={}&podtitle={}&includepodid={}&podstate={}'


def main():

    # Handle type
    _type = int(input(
        '\nSelect Problem Type:'
            '\n[1] Indefinite Integral'
            '\n[2] Definite Integral'
            '\n[3] Derivative'
            '\n>>> '
                 ))
    if not 4 > _type > 0:
        raise Exception('Wrong type!')
    
    # Handle input
    _input = input('\nEnter Wolfram Integral URL: ')
    query = _input.split('/input/?i=')[-1]

    print('\nConnecting to Wolfram Alpha...')
    
    # Get XML page
    # May take up to 10 seconds depending on your ping and
    # the computation required based on Integral complexity
    wolfram_url = URL.format(appid, query, *Headers[_type])
    xml = urlopen(wolfram_url).read().decode()
    xml_nice = xml.replace('\n', '').replace(' ', '')

    # Regex it to get solution
    regex = re.findall(r"(?<=Possibleintermediatesteps'><imgsrc=')(.*)(?='alt=')", xml_nice)

    # Handle Result
    img_url = None if not regex else regex[0]
    if not img_url:
        raise Exception('Error while getting result!')

    # Removing 'amp;' to avoid connection issue
    img_url = img_url.replace('amp;', '')

    # Change extension from gif to png
    img_url = img_url.replace('image/gif', 'image/png')
    
    print('Downloading Solution...')
    
    # Download Solution
    img_name = img_url.split('/MSP/')[-1].split('?')[0] + '.png'
    urlretrieve(img_url, img_name)

    print('Saved at: {}\\{}'.format(os.getcwd(), img_name))



if __name__ == '__main__':
    main()
