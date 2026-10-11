import json,re,urllib.request,urllib.parse,pathlib,shutil,sys,time
ROOT=pathlib.Path(__file__).resolve().parent.parent
VIDEO={'.mp4':'video/mp4','.m4v':'video/mp4','.webm':'video/webm','.mov':'video/quicktime','.mkv':'video/x-matroska','.mpeg':'video/mpeg','.mpg':'video/mpeg','.avi':'video/x-msvideo','.ogv':'video/ogg','.ts':'video/mp2t'}
IMAGES={'.jpg','.jpeg','.png','.gif','.webp','.avif','.bmp','.svg','.ico'}
def folder_config(value):
 u=urllib.parse.urlsplit(value)
 if u.scheme!='https' or u.hostname not in ['filedn.eu','filedn.com'] or u.username or u.password or u.port or u.query or u.fragment or not re.fullmatch(r'/[A-Za-z0-9]+(?:/[^?#]*)?',u.path):raise ValueError('Use a pCloud Public Folder directory link from filedn.eu or filedn.com.')
 return value.rstrip('/')+'/'
def index_folder(base,kind):
 base=folder_config(base);visited=set();count=0
 def visit(path='',depth=0):
  nonlocal count
  if depth>30 or len(visited)>500:raise ValueError('Folder limit exceeded.')
  url=base+('/'.join(urllib.parse.quote(x,safe='') for x in path.split('/'))+'/' if path else '')
  if url in visited:raise ValueError('Repeated directory.')
  visited.add(url)
  request=urllib.request.Request(url,headers={'User-Agent':'LarsGade-GitHub-Pages/1.0'})
  with urllib.request.urlopen(request,timeout=25) as response:
   final=urllib.parse.urlsplit(response.url)
   if final.hostname not in ['filedn.eu','filedn.com']:raise ValueError('Invalid directory redirect.')
   html=response.read(2_000_001).decode('utf-8')
  if len(html)>2_000_000:raise ValueError('Directory too large.')
  match=re.search(r'(?:var|let|const)\s+directLinkData\s*=\s*(\{[\s\S]*?\})\s*;?\s*</script>',html)
  if not match:raise ValueError('Could not read the Public Folder directory.')
  items=json.loads(match.group(1)).get('content',[]);contents=[]
  for entry in items:
   name=entry.get('name','')
   if not isinstance(name,str) or not name or name in ['.','..'] or any(x in name for x in ['/','\\']) or any(ord(x)<32 for x in name):continue
   rel=(path+'/' if path else '')+name;ext=pathlib.PurePosixPath(name).suffix.lower();count+=1
   if count>10000:raise ValueError('File limit exceeded.')
   if entry.get('size') is None:
    contents.append(visit(rel,depth+1));continue
   if kind=='videos' and ext not in VIDEO:continue
   if kind=='images' and ext not in IMAGES:continue
   direct=base+'/'.join(urllib.parse.quote(x,safe='') for x in rel.split('/'))
   contents.append({'id':rel,'fileid':rel,'name':name,'isfolder':False,'size':entry['size'],'publicPath':rel,'streamUrl':direct,'downloadUrl':direct,'type':VIDEO.get(ext,'application/octet-stream')})
  return {'id':path or 'public-root','folderid':path or 'public-root','name':path.split('/')[-1] if path else {'files':'Files','videos':'Videos','images':'Images'}[kind],'isfolder':True,'publicPath':path,'contents':contents}
 return visit()
def build():
 config=json.loads((ROOT/'site-config.json').read_text());out=ROOT/'_site';shutil.rmtree(out,ignore_errors=True);out.mkdir()
 for path in ROOT.iterdir():
  if path.name in ['assets'] and path.is_dir():shutil.copytree(path,out/path.name)
  elif path.is_file() and (path.suffix in ['.html','.css','.js'] or path.name in ['.nojekyll','CNAME','site-config.json']):shutil.copy2(path,out/path.name)
 result={'generatedAt':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'sections':{}};errors=[]
 for kind in ['files','videos','images']:
  value=config.get(kind,{}).get('url','').strip()
  if not value:result['sections'][kind]={'tree':None};continue
  try:result['sections'][kind]={'tree':index_folder(value,kind)}
  except Exception as e:errors.append(kind+': '+str(e))
 if errors:
  print('\n'.join(errors),file=sys.stderr);raise SystemExit('Folder refresh failed; previous deployment remains active. Correct the link in admin and save again.')
 (out/'folder-index.json').write_text(json.dumps(result,ensure_ascii=False));print('Static site prepared.')
if __name__=='__main__':build()
