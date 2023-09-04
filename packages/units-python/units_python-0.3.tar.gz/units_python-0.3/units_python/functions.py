import re

def fraction_decoder(fraction):
    fraction = remove_excess_spaces(fraction)

    if '/' in fraction: 
        parts = fraction.split('/')
        if len(parts) != 2: raise ValueError("Input must have exactly one '/' character to separate numerator and denominator.")
    else:
        parts = [fraction, ""]
    
    pattern = r'(?<=[A-Za-z0-9])\*(?=[A-Za-z0-9])'
    nominator = re.split(pattern, parts[0])
    denominator = re.split(pattern, parts[1])
    
    nominator = [item.strip().strip("()") for item in nominator if item.strip()]
    denominator = [item.strip().strip("()") for item in denominator if item.strip()]
    
    return nominator, denominator

def remove_excess_spaces(input_string):
    result = []
    i = 0
    while i < len(input_string):
        if input_string[i] == " ":
            if i + 1 > len(input_string) - 1:
                break
            if input_string[i+1] in ('*', '/') or input_string[i-1] in ('*', '/'):
                i += 1
                continue
        result.append(input_string[i])
        i += 1
    return ''.join(result)

if __name__ == "__main__":
    fraction = "(5 m * 10 ton)/5 h**2*20 m*10 liter"
    print(*fraction_decoder(fraction), sep="\n")