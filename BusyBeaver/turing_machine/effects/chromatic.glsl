// 采样密度
const int SAMPLES = 32;
const float GOLDEN_ANGLE = 2.3999632;

vec4 scene_color = texture(fbo, v_texcoord);
vec3 final_glow = vec3(0.0);

// 模拟色散
vec3 chromatic_weights = vec3(1.0, 1.02, 1.05); 
float total_weight = 0.0;

// 亮度系数
const vec3 luma_coeff = vec3(0.2126, 0.7152, 0.0722);

// 螺旋采样
for (int i = 0; i < SAMPLES; i++) {
    float f_i = float(i);
    float progress = f_i / float(SAMPLES);
    
    float weight = exp(-progress * 3.0); 
    
    // 旋转角度，偏移
    float angle = f_i * GOLDEN_ANGLE;
    float curr_radius = progress * radius;
    vec2 offset = vec2(cos(angle), sin(angle)) * curr_radius;
    
    // R
    vec3 tex_r = texture(fbo, v_texcoord + offset * chromatic_weights.r).rgb;
    float luma_r = dot(tex_r, luma_coeff);
    float r = (luma_r < threshold) ? 0.0 : tex_r.r;

    // G
    vec3 tex_g = texture(fbo, v_texcoord + offset * chromatic_weights.g).rgb;
    float luma_g = dot(tex_g, luma_coeff);
    float g = (luma_g < threshold) ? 0.0 : tex_g.g;

    // B
    vec3 tex_b = texture(fbo, v_texcoord + offset * chromatic_weights.b).rgb;
    float luma_b = dot(tex_b, luma_coeff);
    float b = (luma_b < threshold) ? 0.0 : tex_b.b;

    final_glow += vec3(r, g, b) * weight;
    total_weight += weight;
}

final_glow /= total_weight;
final_glow *= intensity;

if (glow_color.a > 0.0) {
    // Screen
    final_glow *= glow_color.rgb;
}

// 防止过曝
vec3 result = scene_color.rgb + final_glow;

f_color = vec4(result, clamp(scene_color.a + length(final_glow), 0.0, 1.0));
