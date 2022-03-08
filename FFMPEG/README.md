#Pipeline to convert video files using FFMPEG 
##Original notes ~ 
>command input options output 
conda create —name ffmpeg
conda activate ffmpeg 
 conda install ffmpeg 
ffprobe filename 
>ffprob info: fps, resolution ( x ), pixel info / how colours are stored (eg RGB or grayscale; 420 for human eye, 444 for all colour data), codec, bitrate (speed necessary from computer - this is what we’re trying to reduce) 
mkdir foldername
	>makes new folder (make directory) 
ffmpeg -i parentfolder\inputfilename -c:v codec -crf parameters parentfolder\outputfilename
	> -i  input 
	> -c:v copy:video, this can be -c:a copy:audio, etc
> codec  libx265, lib265 (allied colour cam), libx264 (choose this option if using VS code & VLC viewer, lib264 (choose this option if using allied colour cam) 
>parameters = higher number more compression, ranges 0-52; 0 = no chg; 18 = ~10%orig size without loss of quality but this will vary. 100mb/min is a good threshold. Sometimes putting low numbers will increase file size; this is because default parameters are used/new codec. 23 is pretty good, play with 18-28 and select 1-2 below what looks good to the eye for the final processed version
ffmpeg -i raw\jwasp_cockroach0.avi processed\jwasp_cockroach0_copy.avi
>copies video into new folder, *but with default parameters, so not the same quality
	>speed  how fast its copying 
ffmpeg -i raw\jwasp_cockroach0.avi -c:v copy processed\jwasp_cockroach0_copy.avi
>*this copies in the same original parameters resulting in the same video
ffmpeg -i raw\jwasp_cockroach0.avi -ss 00:01:15 -to 00:01:30 processed\jwasp_cockroach0_short.avi
> -ss = start time with format hr:min:sec
> -to = end time
>*will be default codec unless you specify -c:v copy like above 
ffmpeg -i raw\jwasp_cockroach0.avi -c:v libx264 -ss 00:01:15 -to 00:01:30 processed\jwasp_cockroach0_short264.avi 
