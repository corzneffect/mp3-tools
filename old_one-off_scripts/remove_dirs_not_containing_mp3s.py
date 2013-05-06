import os

def cleanup(d):
    fl=os.listdir(d)
    can_delete=True
    if len(fl)==0:
        print '%s is empty' %d
    else:
        
        for f in fl:
            newd=os.path.join(d,f)
            if os.path.isdir(newd):
                if not cleanup(newd):
                    can_delete=False
            elif f[-4:]=='.mp3':
                can_delete=False
        
    if can_delete:
        print 'Deleting %s' %d
        os.system('rm -rf "%s"' %d)
    return can_delete

cleanup('/home/cory/mp3')
