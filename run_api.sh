export api_ip=$(dig TXT +short o-o.myaddr.l.google.com @ns1.google.com) 
export bugsnag_key=$(cat /home/deno/.bugsnagconf)
export aws_id=$(head -n 1 /home/deno/.aws_creds)
export aws_key=$(head -n 2 /home/deno/.aws_creds)
python api.py

