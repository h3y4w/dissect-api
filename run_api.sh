echo 'find a way to get api IP, set it as localhost'
export api_ip='localhost'
export bugsnag_key=$(cat /home/deno/.bugsnagconf)
export aws_id=$(sed -n '1p' /home/deno/.aws_creds)
export aws_key=$(sed -n '2p' /home/deno/.aws_creds)
export port=5000
python api.py

