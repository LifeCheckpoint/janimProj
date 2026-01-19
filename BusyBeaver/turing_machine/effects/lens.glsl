// float lens_strength = 0.2; // 扭曲强度，正值中心放大，负值中心缩小
// float lens_radius = 0.5;   // 透镜作用半径
// float aspect_ratio = 1.77; // 宽高比修正

vec2 uv = v_texcoord - vec2(0.5);
uv.x *= aspect_ratio;

float dist = length(uv);          // 计算当前点到中心的距离

if (dist < lens_radius) {
    // 重映射距离
    float percent = dist / lens_radius;
    
    // 凸透镜算法
    float distortion = 1.0 + lens_strength * (1.0 - pow(percent, 2.0));
    
    // 只有在半径内才进行偏移
    uv /= distortion; 
}

// 还原坐标
uv.x /= aspect_ratio;
vec2 new_v_texcoord = uv + vec2(0.5);

vec4 scene_color = texture(fbo, new_v_texcoord);

f_color = scene_color;
