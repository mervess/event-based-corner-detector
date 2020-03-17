import numpy as np


class FastDetector:

    def __init__( self ):
        # parameters
        self.sensor_width = 240;
        self.sensor_height = 180;

        # SAE = Surface of Active Events
        self.sae_0 = np.zeros( (self.sensor_width, self.sensor_height) ) # for polarity 0
        self.sae_1 = np.zeros( (self.sensor_width, self.sensor_height) ) # for polarity 1

        # pixels on circle
        self.circle_3 = np.matrix( [ [0, 3], [1, 3], [2, 2], [3, 1],
                                     [3, 0], [3, -1], [2, -2], [1, -3],
                                     [0, -3], [-1, -3], [-2, -2], [-3, -1],
                                     [-3, 0], [-3, 1], [-2, 2], [-1, 3] ] ) # 16 rows, 2 columns
        self.circle_4 = np.matrix( [ [0, 4], [1, 4], [2, 3], [3, 2],
                                     [4, 1], [4, 0], [4, -1], [3, -2],
                                     [2, -3], [1, -4], [0, -4], [-1, -4],
                                     [-2, -3], [-3, -2], [-4, -1], [-4, 0],
                                     [-4, 1], [-3, 2], [-2, 3], [-1, 4] ] ) # 20 rows, 2 columns

    
    def clear( self ):
        self.sae_0 = np.zeros_like( self.sae_0 )
        self.sae_1 = np.zeros_like( self.sae_1 )
    
    
    def is_feature( self, x, y, t, p ):
        # update SAE

        # print( "%d, %d, %f, %d" % (x, y, t, p) )

        sae = self.sae_0 if p == 0 else self.sae_1
        sae[x, y] = t 

        max_scale = 1

        # check whether it is not too close to the border
        cs = max_scale*4
        # if ( y < cs or y >= self.sensor_width-cs or
        #      x < cs or x >= self.sensor_height-cs ): # burasi degisti x-y olarak
        #      return False
        
        if ( x < cs or x >= self.sensor_width-cs or
                y < cs or y >= self.sensor_height-cs ): # burasi degisti x-y olarak
            return False
             
        found_streak = False

        # start with circle_3
        for i in range(16):
            for streak_size in range(3, 7):
                # check whether first event is larger than its neighbor
                if sae[x+self.circle_3[i, 0], y+self.circle_3[i, 1]] < sae[x+self.circle_3[(i-1+16)%16, 0], y+self.circle_3[(i-1+16)%16, 1]]:
                    continue

                if sae[x+self.circle_3[(i+streak_size-1)%16, 0], y+self.circle_3[(i+streak_size-1)%16, 1]] < sae[x+self.circle_3[(i+streak_size)%16, 0], y+self.circle_3[(i+streak_size)%16, 1]]:
                    continue

                min_t = sae[x+self.circle_3[i, 0], y+self.circle_3[i, 1]]
                for j in range(1, streak_size):
                    tj = sae[x+self.circle_3[(i+j)%16, 0], y+self.circle_3[(i+j)%16, 1]]
                    if tj < min_t:
                        min_t = tj

                did_break = False
                for j in range(streak_size, 16):
                    tj = sae[x+self.circle_3[(i+j)%16, 0], y+self.circle_3[(i+j)%16, 1]]
                    if tj >= min_t:
                        did_break = True
                        break

                if not did_break:
                    found_streak = True
                    break

            if found_streak:
                break

        # continue with circle_4
        if found_streak:
            found_streak = False
            for i in range(20):
                for streak_size in range(4, 9):
                    # check whether first event is larger than its neighbor
                    if sae[x+self.circle_4[i, 0], y+self.circle_4[i, 1]] <  sae[x+self.circle_4[(i-1+20)%20, 0], y+self.circle_4[(i-1+20)%20, 1]]:
                        continue

                    if sae[x+self.circle_4[(i+streak_size-1)%20, 0], y+self.circle_4[(i+streak_size-1)%20, 1]] < sae[x+self.circle_4[(i+streak_size)%20, 0], y+self.circle_4[(i+streak_size)%20, 1]]:
                        continue

                    min_t = sae[x+self.circle_4[i, 0], y+self.circle_4[i, 1]];
                    for j in range(1, streak_size):
                        tj = sae[x+self.circle_4[(i+j)%20, 0], y+self.circle_4[(i+j)%20, 1]]
                        if tj < min_t:
                            min_t = tj

                    did_break = False
                    for j in range(streak_size, 20):
                        tj = sae[x+self.circle_4[(i+j)%20, 0], y+self.circle_4[(i+j)%20, 1]]
                        if tj >= min_t:
                            did_break = True
                            break

                    if not did_break:
                        found_streak = True
                        break

                if found_streak:
                    break

        return found_streak


    def debug_control( self ):
        print( type( self.sae_0 ) )
        print( type( self.sae_1 ) )

        print( self.sae_0.dtype )
        print( self.sae_1.dtype )

        print( self.sae_0.ndim )
        print( self.sae_1.ndim )

        print( self.sae_0.size )
        print( self.sae_1.size )

        print( self.sae_0.shape )
        print( self.sae_1.shape )

        print( self.circle_3.shape )
        print( self.circle_4.shape )

    def get_name( self ):
        return "FAST Detector"

if __name__ == '__main__':
    fast = FastDetector()
    fast.debug_control()
