//#include <stdio.h>
//#include <stdlib.h>
//#include "ulcg.h"

#include "util.h"
//#include "config.h"
#include "bbattery.h"
#include "smultin.h"
#include "sknuth.h"
#include "smarsa.h"
#include "snpair.h"
#include "svaria.h"
#include "sstring.h"
#include "swalk.h"
#include "scomp.h"
#include "sspectral.h"
#include "swrite.h"
#include "sres.h"
#include "unif01.h"
#include "ufile.h"

#include "gofs.h"
#include "gofw.h"
#include "fdist.h"
#include "fbar.h"
#include "num.h"
#include "chrono.h"

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <limits.h>

#define THOUSAND 1000
#define MILLION (THOUSAND * THOUSAND)
#define BILLION (THOUSAND * MILLION)



int main( int argc, char *argv[] )  {
    unif01_Gen *gen;
    double nb;
    long bufsiz;
    char *fname;
    int NbDelta = 1;
    double ValDelta[] = { 1 };
    long n, L;
    int r = 0;
    int s = 32;
    long N = 1;
    double z;

   if( argc == 3 || argc == 4 ) {
      printf("The arguments supplied are %s %s\n", argv[1],argv[2]);
      if( argc == 3){
        nb = 10000000000;
      }
      if(argc == 4){
        nb = atoi(argv[3]);}
      nb -= fmod (nb, 32.0);
      bufsiz = nb / 32.0;
      fname = argv[1];
      gen=ufile_CreateReadBin(fname,bufsiz);
      ufile_InitReadBin();

      switch(atoi(argv[2])) {

        case 0 :
            bbattery_Alphabit(gen,nb/2,0,32);
            break;
        
        case 1 :  //MultinomialBitsOver, L = 2
            {
                smultin_Param *par = NULL;
                smultin_Res *res;
                par = smultin_CreateParam (NbDelta, ValDelta, smultin_GenerCellSerial, 3);
                res = smultin_CreateRes (par);

                ufile_InitReadBin ();

                if (nb > BILLION)
                    N = 1 + nb / BILLION;
                else
                    N = 1;
                n = nb / N;
                /* Set n as a multiple of s = 32 */
                n -= n % 32;
                smultin_MultinomialBitsOver (gen, par, res, N, n, r, s, 2, FALSE);

                smultin_DeleteRes (res);
                smultin_DeleteParam (par);
            }
            break;

        case 2 : //MultinomialBitsOver, L = 4
            {
                smultin_Param *par = NULL;
                smultin_Res *res;
                par = smultin_CreateParam (NbDelta, ValDelta, smultin_GenerCellSerial, 3);
                res = smultin_CreateRes (par);

                ufile_InitReadBin ();

                if (nb > BILLION)
                    N = 1 + nb / BILLION;
                else
                    N = 1;
                n = nb / N;
                /* Set n as a multiple of s = 32 */
                n -= n % 32;
                smultin_MultinomialBitsOver (gen, par, res, N, n, r, s, 4, FALSE);

                smultin_DeleteRes (res);
                smultin_DeleteParam (par);
            }
            break;

        case 3 : //MultinomialBitsOver, L = 8
            {
                smultin_Param *par = NULL;
                smultin_Res *res;
                par = smultin_CreateParam (NbDelta, ValDelta, smultin_GenerCellSerial, 3);
                res = smultin_CreateRes (par);

                ufile_InitReadBin ();

                if (nb > BILLION)
                    N = 1 + nb / BILLION;
                else
                    N = 1;
                n = nb / N;
                /* Set n as a multiple of s = 32 */
                n -= n % 32;
                smultin_MultinomialBitsOver (gen, par, res, N, n, r, s, 8, FALSE);

                smultin_DeleteRes (res);
                smultin_DeleteParam (par);
            }
            break;

        case 4 : //MultinomialBitsOver, L = 16
            {
                smultin_Param *par = NULL;
                smultin_Res *res;
                par = smultin_CreateParam (NbDelta, ValDelta, smultin_GenerCellSerial, 3);
                res = smultin_CreateRes (par);

                ufile_InitReadBin ();

                if (nb > BILLION)
                    N = 1 + nb / BILLION;
                else
                    N = 1;
                n = nb / N;
                /* Set n as a multiple of s = 32 */
                n -= n % 32;
                smultin_MultinomialBitsOver (gen, par, res, N, n, r, s, 16, FALSE);

                smultin_DeleteRes (res);
                smultin_DeleteParam (par);
            }
            break;

        case 5: //HammingIndep, L = 16
            {
                sstring_Res *res;
                res = sstring_CreateRes();
                ufile_InitReadBin ();
                z = nb / s;
                N = 1 + z / BILLION;
                n = z / N;
                sstring_HammingIndep (gen, res, N, n, r, s, 16, 0);
                sstring_DeleteRes(res);
            }
            break;

        case 6: //HammingIndep, L = 32
            {
                sstring_Res *res;
                res = sstring_CreateRes();
                ufile_InitReadBin ();
                z = nb / s;
                N = 1 + z / BILLION;
                n = z / N;
                n /= 2;
                sstring_HammingIndep (gen, res, N, n, r, s, 32, 0);
                sstring_DeleteRes(res);
            }
            break;

        case 7: //HammingCorr, L = 32
            {
                sstring_Res *res;
                res = sstring_CreateRes();
                ufile_InitReadBin ();
                z = nb / s;
                N = 1 + z / BILLION;
                n = z / N;
                sstring_HammingCorr (gen, res, N, n, r, s, 32);
                sstring_DeleteRes(res);
            }
            break;

        case 8: //RandomWalk1, L = 64
            {
                swalk_Res *res;
                res = swalk_CreateRes ();
                ufile_InitReadBin ();
                L = 64;
                z = nb / L;
                N = 1 + z / BILLION;
                n = z / N;
                swalk_RandomWalk1 (gen, res, N, n, r, s, L, L);
                swalk_DeleteRes (res);
            }
            break;
        case 9: //RandomWalk1, L = 320
            {
                swalk_Res *res;
                res = swalk_CreateRes ();
                ufile_InitReadBin ();
                L = 320;
                z = nb / L;
                N = 1 + z / BILLION;
                n = z / N;
                swalk_RandomWalk1 (gen, res, N, n, r, s, L, L);
                swalk_DeleteRes (res);
            }
            break;
        case 10: //SmallCrush BirthdaySpacings
            {
                sres_Poisson *res;
                res = sres_CreatePoisson ();
                ufile_InitReadBin ();
                smarsa_BirthdaySpacings (gen, res, 1, 5 * MILLION, r, 1073741824, 2, 1);
                sres_DeletePoisson (res);
            }
            break;
        case 11: //SmallCrush Collision
            {
                sknuth_Res2 *res;
                res = sknuth_CreateRes2 ();
                ufile_InitReadBin ();
                sknuth_Collision (gen, res, 1, 5 * MILLION, 0, 65536, 2);
                sknuth_DeleteRes2 (res);
            }
            break;
        case 12: //SmallCrush Gap
            {
                sres_Chi2 *res;
                res = sres_CreateChi2 ();
                ufile_InitReadBin ();
                sknuth_Gap (gen, res, 1, MILLION / 5, 22, 0.0, .00390625);
                sres_DeleteChi2 (res);
            }
            break;
        case 13: //SmallCrush SimpPoker
            {
                sres_Chi2 *res;
                res = sres_CreateChi2 ();
                ufile_InitReadBin ();
                sknuth_SimpPoker (gen, res, 1, 2 * MILLION / 5, 24, 64, 64);
                sres_DeleteChi2 (res);
            }
            break;
        case 14: //SmallCrush CouponCollector
            {
                sres_Chi2 *res;
                res = sres_CreateChi2 ();
                ufile_InitReadBin ();
                sknuth_CouponCollector (gen, res, 1, MILLION / 2, 26, 16);
                sres_DeleteChi2 (res);
            }
            break;
        case 15: //SmallCrush MaxOft
            {
                sknuth_Res1 *res;
                res = sknuth_CreateRes1 ();
                ufile_InitReadBin ();
                sknuth_MaxOft (gen, res, 1, 2 * MILLION, 0, MILLION / 10, 6);
                sknuth_DeleteRes1 (res);
            }
            break;
        case 16: //SmallCrush WeightDistrib
            {
                sres_Chi2 *res;
                res = sres_CreateChi2 ();
                ufile_InitReadBin ();
                svaria_WeightDistrib (gen, res, 1, MILLION / 5, 27, 256, 0.0, 0.125);
                sres_DeleteChi2 (res);
            }
            break;
        case 17: //SmallCrush MatrixRank
            {
                sres_Chi2 *res;
                res = sres_CreateChi2 ();
                ufile_InitReadBin ();
                smarsa_MatrixRank (gen, res, 1, 20 * THOUSAND, 20, 10, 60, 60);
                sres_DeleteChi2 (res);
            }
            break;
        case 18: //SmallCrush HammingIndep
            {
                sstring_Res *res;
                res = sstring_CreateRes();
                ufile_InitReadBin ();
                sstring_HammingIndep (gen, res, 1, MILLION/2, 20, 10, 300, 0);
                sstring_DeleteRes(res);
            }
            break;
        case 19: //SmallCrush RandomWalk1
            {
                swalk_Res *res;
                res = swalk_CreateRes ();
                ufile_InitReadBin ();
                L = 320;
                z = nb / L;
                N = 1 + z / BILLION;
                n = z / N;
                swalk_RandomWalk1 (gen, res, 1, MILLION, r, 30, 150, 150);
                swalk_DeleteRes (res);
            }
            break;

        case 20 : //Rabbit battery
            bbattery_Rabbit(gen,nb/2);
            break;
        

        }
    
      ufile_DeleteReadBin(gen);
   }
   else if( argc > 4 ) {
      printf("Too many arguments supplied.\n");
   }
   else {
      printf("Expected format %s <filename> <testnum> <length>\n",argv[0]);
   }




}