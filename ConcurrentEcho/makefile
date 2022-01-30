echoThread: csapp.o echo.o echoThread.o
	gcc -pthread csapp.o echo.o ./server/echoThread.o -o ./server/echoThread 

echoThread.o: ./server/echoThread.c csapp.h
	gcc -c ./server/echoThread.c -o ./server/echoThread.o

echoIOMultiplex: csapp.o echo.o echoIOMultiplex.o
	gcc -pthread csapp.o echo.o ./server/echoIOMultiplex.o -o ./server/echoIOMultiplex 

echoIOMultiplex.o: ./server/echoIOMultiplex.c csapp.h
	gcc -c ./server/echoIOMultiplex.c -o ./server/echoIOMultiplex.o

echoProcess: csapp.o echo.o echoProcess.o
	gcc -pthread csapp.o echo.o ./server/echoProcess.o -o ./server/echoProcess
	
echoProcess.o: ./server/echoProcess.c csapp.h
	gcc -c ./server/echoProcess.c -o ./server/echoProcess.o

echoIterative: csapp.o echo.o echoIterative.o
	gcc -pthread csapp.o echo.o ./server/echoIterative.o -o ./server/echoIterative

echoIterative.o: ./server/echoIterative.c csapp.h
	gcc -c ./server/echoIterative.c -o ./server/echoIterative.o

echoclient: csapp.o echo.o echoclient.o
	gcc -pthread csapp.o echo.o echoclient.o -o echoclient

csapp.o: csapp.h csapp.c
	gcc -c csapp.c

echo.o: echo.c csapp.h
	gcc -c echo.c

echoclient.o: echoclient.c csapp.h
	gcc -c echoclient.c

clean:
	rm *.o ./server/*.o echoclient ./server/echoIterative ./server/echoProcess ./server/echoIOMultiplex ./server/echoThread  