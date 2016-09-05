export api_ip=$(dig TXT +short o-o.myaddr.l.google.com @ns1.google.com) 
export bugsnag_key=$(cat /home/deno/.bugsnagconf)
python api.py
