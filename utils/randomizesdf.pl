#!/usr/bin/perl

	my($file,$fileout)=@ARGV;

	if($file eq "" || $fileout eq ""){
                die "usage: <>.pl <input sdf file> <output sdf file> create a reoriented sdf file\n";
        };

	#matrix
	@tab='';
	$degree=int(rand(180));
        $fa=cos($degree);
        $fa1=sin($degree);
        $fa2=0;
        $fb=-sin($degree);
        $fb1=cos($degree);
        $fb2=0;
        $fc=0;
        $fc1=0;
        $fc2=1;
	$fd=rand(5);
        $fe=rand(1);
        if($fe <= 0.5){
        	$fd=$fe * -1;
        };
	$tab[0]=$fa;
	$tab[1]=$fa1;
	$tab[2]=$fa2;
	$tab[3]=$fd;
	$fd=rand(5);
	$fe=rand(1);
	if($fe <= 0.5){
		$fd=$fe * -1;
        };
	$tab[4]=$fb;
	$tab[5]=$fb1;
	$tab[6]=$fb2;
	$tab[7]=$fd;	
	$fd=rand(5);
        $fe=rand(1);
        if($fe <= 0.5){
        	$fd=$fe * -1;
        };
	$tab[8]=$fc;
	$tab[9]=$fc1;
	$tab[10]=$fc2;
	$tab[11]=$fd;
	$tab[12]=0.0;
	$tab[13]=0.00;
	$tab[14]=0.00;
	$tab[15]=1.00;

	open(OUT,">$fileout");
	$flagnew=1;
	open(MOL,"<$file");
	while(<MOL>){
                if($flagnew){
                        $compt=0;
                        $ig=1;
                        $jg=0;
                        @strx='';
                        @stry='';
                        @strz='';
                        @atom='';
                        $blanc=' ';
			$zero='0';
                        $flagnew=0;
                };
                @getstr = split(' ',$_);
                $compt++;

		if ($compt < 4){
			print OUT $_;
		};

                if (($compt > 4) && ($ig <= $istratom)){
                        $strx[$ig]=$getstr[0];
                        $stry[$ig]=$getstr[1];
                        $strz[$ig]=$getstr[2];
                        $atom[$ig]=$getstr[3];
	
			$suite="";
			foreach $k (4..@getstr-1){
				$suite=$suite."  ".$getstr[$k];
			};

			$x=$strx[$ig]*$tab[0]+$stry[$ig]*$tab[1]+$strz[$ig]*$tab[2]+$tab[3];
			$y=$strx[$ig]*$tab[4]+$stry[$ig]*$tab[5]+$strz[$ig]*$tab[6]+$tab[7];
			$z=$strx[$ig]*$tab[8]+$stry[$ig]*$tab[9]+$strz[$ig]*$tab[10]+$tab[11];
			$x=sprintf "%4.3f",$x;
			$y=sprintf "%4.3f",$y;
			$z=sprintf "%4.3f",$z;

			printf OUT "%10s%10s%10s%1s%1s $suite\n",$x,$y,$z,$blanc,$getstr[3];
                        $ig++;

                };

                if (($compt > 4) && ($ig > $istratom) && ($jg <=$istrbond)){
			if ($jg == 0){
                                $jg++;
                        }
                        else{
				$jg++;
				print OUT $_;
			};
		}
		elsif(($compt > 4) && ($ig > $istratom) && ($jg > $istrbond)){
			print OUT $_;
		};

                if ($compt == 4){
                        $istratom=$getstr[0];
                        $istrbond=$getstr[1];

                        @coller=split(' *',$istratom);
                        if(@coller>3 && @coller==6){
                                $istratom=$coller[0].$coller[1].$coller[2];
                                $istrbond=$coller[3].$coller[4].$coller[5];
                        }
                        elsif(@coller>3 && @coller==5){
                                if($_=~/^\s/){
                                        $istratom=$coller[0].$coller[1];
                                        $istrbond=$coller[2].$coller[3].$coller[4];
                                }
                                else{
                                        $istratom=$coller[0].$coller[1].$coller[2];
                                        $istrbond=$coller[3].$coller[4];
                                };
                        };
			print OUT $_;
                };

		if($_=~/\$\$\$\$/){
			$flagnew=1;
		};
	};
	close(MOL);
	close(OUT);
