
import cli

def main():
    out = ' -o d:/mydocs/tmp/out.png'
    cmd = '--help'
    cmd = '-p source=sample/sample.scc'+out
    cmd = r'-cs MarsNI2001 -p source=D:\mydocs\tmp\test_opencratertools\test1.scc -p type=bpois,range=[8,20]' + out
    cmd = r'-pr cumul -cs neukumivanov -p source=sample\sample.binned'

    
    print(f'\nDebugging command: craterstats '+cmd)
    a = cmd.split()
    cli.main(a)

if __name__ == '__main__':
    main()