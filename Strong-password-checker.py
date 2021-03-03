class Solution:
    def strongPasswordChecker(self, password: str) -> int:
        def func1(password):
            up,lo,di,ld=0,0,0,0
            if len(password)<6:
                ld=len(password)-6
            elif len(password)>20:
                ld=len(password)-20
            for i in password:
                if i.isupper():
                    up+=1
                elif i.islower():
                    lo+=1
                elif i.isdigit():
                    di+=1
            return up,lo,di,ld

        def mid(password,up,lo,di,ld):
            n=0   #n: number of changes for repeating char
            i=0
            n2=0    #n2: number of changes to have all three types
            if up==0:
                n2+=1
            if lo==0:   #ld: number of changes to be 8-20 long
                n2+=1
            if di==0:
                n2+=1

            while i < len(password)-2:
                if password[i]==password[i+1] and password[i+1]==password[i+2]:
                    #found new repeating
                    j=i+3
                    while j<len(password) and password[j]==password[i]: #if still repeating 
                        j+=1
                    #j=first char after repeating
                    #3,4,5:r1,6,7,8:r2,9,10,11,r3...
                    n+=(j-i)//3
                    i=j

                else:
                    i+=1


            return max(n,n2,-ld)
        
        def trimR(password):
            r0=[]
            r1=[]
            r2=[]

            i=0
            while i < len(password)-2:
                if password[i]==password[i+1] and password[i+1]==password[i+2]:
                    #found new repeating
                    j=i+3
                    while j<len(password) and password[j]==password[i]: #if still repeating 
                        j+=1
                    #j=first char after repeating, j-i=length
                    #too long : delete>replace>add
                    if (j-i)%3==0:
                        r0+=[(i,j-i)]
                    elif (j-i)%3==1:
                        r1+=[(i,j-i)]
                    else:
                        r2+=[(i,j-i)]

                    i=j
                else:
                    i+=1

            ld=len(password)-20

            while ld>0:#still need to remove
                #print(password,ld)
                #print(r0,r1,r2)
                if r0!=[]:#if has r0
                    (i,l)=r0[0]
                    password=password[:i]+'X'+password[i+1:]
                    ld-=1
                    if l>3:
                        r2+=[(i+1,l-1)]
                    del r0[0]
                elif r1!=[]:
                    (i,l)=r1[0]
                    password=password[:i]+'X'+password[i+1:]
                    ld-=1
                    r0+=[(i+1,l-1)]
                    del r1[0]
                elif r2!=[]:
                    (i,l)=r2[0]
                    if ld>=2:
                        password=password[:i]+'XX'+password[i+2:]
                        ld-=2
                        r0+=[(i+2,l-2)]
                    else:#ld==1
                        password=password[:i]+'X'+password[i+1:]
                        ld-=1
                        r1+=[(i+1,l-1)]
                    del r2[0]
                else:
                    return password.replace('X','')



            return password.replace('X','') #r0,r1,r2 #
        
        
        def trimT(password):#remove base on types
            up=False
            lo=False
            di=False
            i=0
            while len(password)>20:
                if password[i].isupper():
                    if up:
                        password = password[:i]+password[i+1:]
                    else:
                        up=True
                        i+=1
                elif password[i].islower():
                    if lo:
                        password = password[:i]+password[i+1:]
                    else:
                        lo=True
                        i+=1
                elif password[i].isdigit():
                    if di:
                        password = password[:i]+password[i+1:]
                    else:
                        di=True
                        i+=1
            return password
        
        up,lo,di,ld=func1(password)
        if len(password)<=20:
            return mid(password,up,lo,di,ld)
        else :
            return mid(trimT(trimR(password)),up,lo,di,ld)+ld

