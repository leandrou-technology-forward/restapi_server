def factorial(n,d,s):
    print("n=",n,'d=',d,'s=',s)
    if not d or type(d) == type('') or not (type(d) == type([]) or type(d) == type({}) or type(d) == type(())):
        if type(d) == type(''):
            ds = f"'{d}'"
        else:
            ds=str(d)
        return(0,'',ds)
    else:
        if type(d) == type([]):
            if n < len(d):
                if n == 0:
                    s = s + '['
                w = d[n]
                print('wwwwww', w,'n=',n,'l=',len(d))
                
                if type(w) == type({}):
                    x = 1
                    
                (nn, nd, ns) = factorial(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + ']'
                else:
                    s = s + ', '

                return factorial(n + 1, d, s)
            else:
                return (0,'','')
        elif type(d) == type({}):
            if n < len(d):
                if n == 0:
                    s = s + '{'
                
                keys = list(d.keys())
                k = keys[n]
                w = d.get(k)
                s = s + f"'{k}':"
    
                (nn, nd, ns) = factorial(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + '}'
                else:
                    s = s + ', '

                return factorial(n + 1, d, s)
            else:
                return (0, '', s)
        else:
            return(0,'',s)

#print(factorial(0, ['aaaa', ['1111', 3.345, '3333', ['1', '2', '3']], 'cccc', {'xxxx':1111, 'zzzzz':3333}], ''))

def decorated_data_recursion(n,d,s):
    # print("n=",n,'d=',d,'s=',s)
    if not d or type(d) == type('') or not (type(d) == type([]) or type(d) == type({}) or type(d) == type(())):
        if type(d) == type(''):
            ds = f"'{d}'"
        else:
            ds=str(d)
        return(0,'',ds)
    else:
        if type(d) == type([]):
            if n < len(d):
                if n == 0:
                    s = s + '['
                w = d[n]
                # print('next item:', w,'n=',n,'l=',len(d))
                
                (nn, nd, ns) = decorated_data_recursion(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + ']'
                else:
                    s = s + ', '

                return decorated_data_recursion(n + 1, d, s)
            else:
                return (0,'',s)
        elif type(d) == type({}):
            if n < len(d):
                if n == 0:
                    s = s + '{'
                
                keys = list(d.keys())
                k = keys[n]
                w = d.get(k)
                s = s + f"'{k}':"
    
                (nn, nd, ns) = decorated_data_recursion(0, w, '')
                
                s = s + ns

                if n >= len(d)-1:
                    s = s + '}'
                else:
                    s = s + ', '

                return decorated_data_recursion(n + 1, d, s)
            else:
                return (0, '', s)
        else:
            return(0,'',s)

def decorated_data(data):
    (dummy1, dummy2, thisText) = decorated_data_recursion(0, data, '')
    thisText=thisText.replace('[','[#C9#')
    thisText=thisText.replace(']',']#C0#')
    thisText=thisText.replace('{','#C9#{')
    thisText=thisText.replace('}','}#C0#')
    return thisText

this_data = ['aaaa', ['1111', 3.345, '3333', ['1', '2', '3']], 'cccc', {'xxxx':1111, 'zzzzz':3333}]
print(decorated_data(this_data))
