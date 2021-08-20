function matlabRecorder()
    global marker
    marker = "";
    tcpipClient = tcpip('localhost',5002,'NetworkRole','Client');
    tcpipClient.ReadAsyncMode = 'continuous';
    tcpipClient.Terminator = 10;
    tcpipClient.BytesAvailableFcn = @setMarker;
    tcpipClient.BytesAvailableFcnMode = 'terminator';
    fopen(tcpipClient);
    file_out = fopen("file_out.csv", 'w');
    i = double(0);
    while(1)
        if marker == "terminate"
            break
        elseif marker == ""
            fprintf(file_out, "%d, %s\n", i, "");
        else
            fprintf(file_out, "%d,%s\n", i, marker);
            marker = "";
        end
        i =  i + 1;
        pause(0.1);
    end
    fclose(file_out);
    fclose(tcpipClient)
    
end

function setMarker(obj, event)
    global marker;
    data = fscanf(obj);
    marker = erase(data, char(10));
end

