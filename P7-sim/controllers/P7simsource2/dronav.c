if (dist1 <= dist2) {
        printf("dist1 <= dist2");
        ang = acos(((d1a2*d1a2)+(dist1*dist1)-(d1a1*d1a1))/(2*d1a2*dist1));

        if ((yaw == ang)){
          dir = true;
        }
        if ((yaw < ang)) {
          dir = false;
          switch (dir) {
            case false:
              pitch_disturbance = 0.0;
              yaw_disturbance = -1.0;
              break;
            case true:
              yaw_disturbance = 0.0;
              break;            
          }
        }
        else if ((yaw > ang)) {
          dir = false;
          switch (dir) {
            case false:
              pitch_disturbance = 0.0;
              yaw_disturbance = 1.0;
              break;
            case true:
              yaw_disturbance = 0.0;
              break;            
          }
        }
        
        while (dist1 > 0) {
            pitch_disturbance = 2.0;
            if ((dist1 = 0)) {
                pitch_disturbance = 0.0;
                if ((yaw != yawst)){
                  yaw_disturbance = 1.0;
                  if ((yaw == yawst)) {
                    yaw_disturbance = 0.0;
                  }
                }
            }
        }
    }
    else {
        printf("dist2 < dist1");
        ang = acos(((d2a2*d2a2)+(dist2*dist2)-(d2a1*d2a1))/(2*d2a2*dist1));
        
        if ((yaw == ang)){
          dir = true;
        }
        if ((yaw < ang)) {
          dir = false;
          switch (dir) {
            case false:
              pitch_disturbance = 0.0;
              yaw_disturbance = -1.0;
              break;
            case true:
              yaw_disturbance = 0.0;
              break;            
          }
        }
        else if ((yaw > ang)) {
          dir = false;
          switch (dir) {
            case false:
              pitch_disturbance = 0.0;
              yaw_disturbance = 1.0;
              break;
            case true:
              yaw_disturbance = 0.0;
              break;            
          }
        }
        
        while (dist2 > 0) {
            pitch_disturbance = 2.0;
            if ((dist2 = 0)) {
                pitch_disturbance = 0.0;
                if ((yaw != yawst)) {
                  yaw_disturbance = 1.0;
                  if ((yaw == yawst)) {
                    yaw_disturbance = 0.0;
                  }
              }
          }
      }
   }