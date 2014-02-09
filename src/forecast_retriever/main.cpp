#include <iostream>

#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

int main()
{
	pid_t p=fork();

	if(p)
	{
		if(p==-1)
		{
			exit(0);
		}
		else
		{
			waitpid(p,nullptr,0);
		}
	}
	else
	{
		execl("/usr/bin/wget","wget","www.swpc.noaa.gov/ftpdir/weekly/27DO.txt","--output-document=28.txt","--quiet","\0");
	}

	return 0;
}