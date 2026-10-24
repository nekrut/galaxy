"""Capture actual Galaxy components and validation results in a local browser harness."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('phase',choices=['Before','After']);args=p.parse_args()
out=Path(__file__).resolve().parent
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':1280,'height':940},device_scale_factor=1)
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:5178/connection-repro.html?phase='+args.phase,wait_until='networkidle',timeout=60000)
 page.wait_for_timeout(1500)
 (out/(args.phase.lower()+'-browser-errors.json')).write_text(json.dumps(errors,indent=2)+'\n')
 page.screenshot(path=str(out/(args.phase.lower()+'.png')),full_page=True)
 result=page.evaluate('window.repro || null')
 (out/(args.phase.lower()+'-browser-state.json')).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'phase':args.phase,'state':result,'errors':errors},indent=2))
 browser.close()
 assert result is not None and not errors
 assert len(result['invalid'])==(2 if args.phase=='Before' else 0)
