from concurrent import futures
import grpc
from metadata_pb2 import(
    GetFileMetaDataRequest,
    GetFileMetaDataResponse  
)
import metadata_pb2_grpc

# Meta data service class
class MetadataService(metadata_pb2_grpc.MetadataServicer):
    # File that client is sharing, client’s ip, port number
    metaDataMap = {'a.txt': ["127.0.0.1", 50060],
                   'b.txt': ["127.0.0.1", 50060],
                   'c.txt': ["127.0.0.1", 50061],
                   'd.txt': ["127.0.0.1", 50061],
                   'e.txt': ["127.0.0.1", 50062]}
    
    # Gets meta data such as client ip, port number for given file.
    # Throws error if file is not found
    def GetFileMetaData(self, request, context):
        # Check given file in the map
        if request.file in self.metaDataMap:           
            # get ip and port using given file
            ip, port = self.metaDataMap[request.file]
            
            # print request and response
            print("File meta data request: File {}, File meta data response: Client IP {}, Port {}".format(request.file, ip, port))
            
            # return response containing ip and port
            return GetFileMetaDataResponse(peer_ip_address = ip, peer_port = port)
        else:
            # throw error "File not found"
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
        
def serve():
    # Create a server with a thread pool of 10 workers and unlimited max message length
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options = [
            ('grpc.max_send_message_length', -1),
            ('grpc.max_receive_message_length', -1)
        ])
    
    # Add MetadataService object to server
    metadata_pb2_grpc.add_MetadataServicer_to_server(MetadataService(), server)
    
    # Bind server IP and port
    server.add_insecure_port("[::]:50059")
    
    # Start the server
    server.start()
    
    # Wait for termination
    server.wait_for_termination()

# Check the name for main 
if __name__ == '__main__':
    # Init server process
    serve()