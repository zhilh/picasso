#-*- coding:utf-8 -*-
'''
Created on 2018年10月25日
@author: zhilh
Description: 
'''


def test_pass(self):
    '''用于unittest测试框架内，在case执行完成后，判断测试结果是否通过 '''
    if hasattr(self, '_outcome') :  # Python 3.4+
        result = self.defaultTestResult()  # these 2 methods have no side effects
        self._feedErrorsToResult(result, self._outcome.errors)
    else:  # Python 3.2 - 3.3 or 3.0 - 3.1 and 2.7
        result = getattr(self, '_outcomeForDoCleanups', self._resultForDoCleanups)
        
    error = list2reason(self,result.errors)
    failure = list2reason(self,result.failures)        
    if not error and not failure:
        return True
    else:
        #typ, text = ('ERROR', error) if error else ('FAIL', failure)
        #msg = [x for x in text.split('\n')[1:] if not x.startswith(' ')][0]
        #print("\n%s: %s\n     %s" % (typ, self.id(), msg))
        return False

def list2reason(self, exc_list):
    if exc_list and exc_list[-1][0] is self:
        return exc_list[-1][1]
    
    