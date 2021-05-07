#!/usr/bin/perl

        local($file)=@ARGV;

        if($file eq ""){
                die "usage: <>.pl <.xyzrgb file>\ncreates dots.pdb to visualize in PyMol for example";
	};

	$doti=0;
        open(OUT,">dots.pdb");
       	open(IN,"<$file");
       	while(<IN>){
	       	@get=split(' ',$_);
	       	if($get[3]>0.5 && $get[4]>0.5 && $get[5]>0.5){
			$label=1;
			$elt="H";
		}
		elsif($get[3]>0.5 && $get[4]<0.5 && $get[5]<0.5){
			$label=2;
			$elt="O";
		}
		elsif($get[3]<0.5 && $get[4]>0.5 && $get[5]<0.5){
			$label=3;
			$elt="C";
		}
		else{
			$label=4;
			$elt="N";
		};
                $cx=sprintf "%4.2f",$get[0];
                $cy=sprintf "%4.2f",$get[1];
                $cz=sprintf "%4.2f",$get[2];
		$doti++;
		$debnom="mol";
		$occup=1;
		$bfactor=1;
		printf OUT "HETATM%5s %4s %3s     1    %8s%8s%8s  %4s %5s\n",$doti,$elt,$debnom,$cx,$cy,$cz,$occup,$bfactor;
	};
       	close(IN);
        close(OUT);
	print "See dots.pdb\n";
