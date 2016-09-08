export api_ip=$(dig TXT +short o-o.myaddr.l.google.com @ns1.google.com) 
export bugsnag_key=$(cat /home/deno/.bugsnagconf)
export aws_id=$(sed -n '1p' /home/deno/.aws_creds)
export aws_key=$(sed -n '2p' /home/deno/.aws_creds)
export port=5000
python api.py

