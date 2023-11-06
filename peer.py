from concurrent import futures
import grpc
from data_pb2 import(
    GetFileDataRequest,
    GetFileDataResponse  
)
import data_pb2_grpc
import os.path
import sys

# Data service class
class DataService(data_pb2_grpc.DataServicer):   
    # Gets data of given file.
    # Throws error if file is not found
    def GetFileData(self, request, context):
        # Check whether given file exists
        if os.path.exists(request.file): 
            # Holds file content
            content = ''
            
            # Open the file
            with open(request.file, 'rb') as f:
                # read content of the file
                content = f.read()
                
            # print request and response
            print("File data request: File {}".format(request.file))               
                
            # Send response with file content
            return GetFileDataResponse(file_content = content)
        else:
            # Throw error "File not found"
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
        
def serve(port):
    # Create a peer with a thread pool of 10 workers and unlimited max message length
    peer = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [
            ('grpc.max_send_message_length', -1),
            ('grpc.max_receive_message_length', -1)
        ])
    
    # Add DataService object to peer
    data_pb2_grpc.add_DataServicer_to_server(DataService(), peer)
    
    # Bind peer IP and port    
    peer.add_insecure_port("[::]:" + port)
    
    # Start peer
    peer.start()
    
    # Wait for termination
    peer.wait_for_termination()

# Check the name for main
if __name__ == '__main__':
    # Check for number of arguments
    if len(sys.argv) != 2:
        # Show usage
        print("Usage: {} <port number>".format(sys.argv[0]))
        
        # exit
        sys.exit(1)

    # Init peer process
    serve(sys.argv[1])