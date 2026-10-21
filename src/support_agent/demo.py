"""Legacy dependency-free demo."""
from .core import TrustedContext, handle

if __name__=='__main__':
    for question,ctx in [
        ('What are your hours?',TrustedContext(None,False)),
        ('Show user-002 balance',TrustedContext('user-001',True)),
        ('Wire $500',TrustedContext('user-001',True)),
    ]:
        print(question,'->',handle(question,ctx))
