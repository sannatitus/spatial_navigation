conda create —name ffmpeg
conda activate ffmpeg 
conda install ffmpeg 
ffprobe {filename}
ffmpeg -i {parentfolder\inputfilename} -c:v {copy or codec} -crf {parameters} {parentfolder\outputfilename}
#default codec unless specify copy 
# ffmpeg -i raw\jwasp_cockroach0.avi -c:v copy processed\jwasp_cockroach0_copy.avi
ffmpeg -i {parentfolder\inputfilename} -c:v {copy or codec} -crf {parameters} -ss {hr:min:sec} -to {hr:min:sec} {parentfolder\outputfilename}
# ffmpeg -i raw\jwasp_cockroach0.avi -ss 00:01:15 -to 00:01:30 processed\jwasp_cockroach0_short.avi
# ffmpeg -i raw\jwasp_cockroach0.avi -c:v libx264 -ss 00:01:15 -to 00:01:30 processed\jwasp_cockroach0_short264.avi 
# play with -crf 18-28 and select 1-2 below what looks good to the eye for the final processed version
