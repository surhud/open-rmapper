import pyfits;
import numpy as np;
import subprocess;

def get_sql_output(command_sql,out_table):
    command="java -jar casjobs.jar run -t \"dr10/500\" "+command_sql
    print "Running \n",command;
    subprocess.call(command,shell=1);

    command="java -jar casjobs.jar extract -b mydb.%s -F -type fits -d"%(out_table);
    print "Running \n",command;
    subprocess.call(command,shell=1);
    
    command="java -jar casjobs.jar execute -t \"mydb/1\" -n \"drop query\" \"drop table %s\""%(out_table);
    print "Running \n",command
    subprocess.call(command,shell=1);

# First get the simple table with unique values of runs
sql="select count(*) as counts,run into mydb.Fields_cnt from PhotoTag group by run"
get_sql_output(sql,"Fields_cnt");

hdulist=pyfits.open("mydb.Fields_cnt.fit");
data=hdulist[1].data;
run   =data.field("run");
cnt   =data.field("counts");

for i in range(np.size(run)):
    sql="\"select objid,cmodelmag_i,cmodelmagerr_i, modelMag_u, modelMagErr_u,modelMag_g, modelMagErr_g,modelMag_r, modelMagErr_r,modelMag_i, modelMagErr_i,modelMag_z, modelMagErr_z,ra,dec,extinction_u,extinction_g,extinction_r,extinction_i,extinction_z,specobjid into mydb.Parent_Catalog_%d from Phototag \
where run=%d and cmodelmag_i<21 \
  and flags & dbo.fPhotoFlags('SATUR_CENTER') = 0  \
  and flags & dbo.fPhotoFlags('BRIGHT') = 0 \
  and flags & dbo.fPhotoFlags('DEBLEND_TOO_MANY_PEAKS') = 0   \
  and flags & dbo.fPhotoFlags('NODEBLEND') = 0 \
  and flags & dbo.fPhotoFlags('BLENDED') = 0\""%(run[i],run[i])
  get_sql_output(sql,"Parent_Catalog_%d"%(run[i]));
