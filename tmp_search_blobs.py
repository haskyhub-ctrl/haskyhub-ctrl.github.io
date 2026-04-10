import subprocess

def search_blobs():
    # Get all blobs
    print('Getting blobs...')
    cmd1 = subprocess.run(['git', 'rev-list', '--objects', '--all'], capture_output=True, text=True)
    objects = [line.split()[0] for line in cmd1.stdout.splitlines()]
    cmd2 = subprocess.run(['git', 'fsck', '--unreachable'], capture_output=True, text=True)
    for line in cmd2.stdout.splitlines():
        if 'blob' in line:
            objects.append(line.split()[2])
            
    objects = list(set(objects))
    print(f'Found {len(objects)} blobs. Scanning...')
    
    with subprocess.Popen(['git', 'cat-file', '--batch'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=False) as p:
        for obj in objects:
            p.stdin.write((obj + '\\n').encode('utf-8'))
            p.stdin.flush()
            header = p.stdout.readline().decode('utf-8').strip()
            if header.endswith(' missing'):
                continue
            parts = header.split()
            size = int(parts[2])
            content = p.stdout.read(size)
            p.stdout.read(1) # read trailing newline
            
            try:
                text = content.decode('utf-8')
                if 'THOÁT NẠN THÀNH CÔNG' in text:
                    print(f'MATCH: {obj}')
            except:
                pass

search_blobs()
