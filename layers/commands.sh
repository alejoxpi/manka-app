aws lambda publish-layer-version --layer-name aiofile-transcribe-streamig --description "aiofile y amazon-transcribe" --zip-file "fileb:///home/ec2-user/repos/building-gen-ai-whatsapp-assistant-with-amazon-bedrock-and-python/private-assistant/layers/aiofile-amazon-transcribe.zip" --compatible-runtimes python3.8 python3.9 python3.10 python3.11 python3.12 
aws lambda publish-layer-version --layer-name langchain --description "langchain" --zip-file "fileb:///home/ec2-user/repos/building-gen-ai-whatsapp-assistant-with-amazon-bedrock-and-python/private-assistant/layers/langchain.zip" --compatible-runtimes python3.8 python3.9 python3.10 python3.11 python3.12 
aws lambda publish-layer-version --layer-name librerias-adicionales --description "librerias adicionales" --zip-file "fileb:///home/ec2-user/repos/building-gen-ai-whatsapp-assistant-with-amazon-bedrock-and-python/private-assistant/layers/common.zip" --compatible-runtimes python3.8 python3.9 python3.10 python3.11 python3.12 
