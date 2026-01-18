#version 330 core

in vec2 v_texcoord;
out vec4 f_color;

uniform sampler2D fbo;
uniform float threshold;
uniform float radius;
uniform float intensity;
uniform vec4 glow_color;

uniform bool JA_BLENDING;
uniform sampler2D JA_FRAMEBUFFER;
#[JA_FINISH_UP_UNIFORMS]

// 采样密度
#define SAMPLES 32
#define GOLDEN_ANGLE 2.3999632

vec3 soft_threshold(vec3 color, float threshold) {
    float luma = dot(color, vec3(0.2126, 0.7152, 0.0722));
    if (luma < threshold) return vec3(0.0);
    return color;
}

void main()
{
    vec4 scene_color = texture(fbo, v_texcoord);
    vec3 final_glow = vec3(0.0);
    
    // 模拟色散
    vec3 chromatic_weights = vec3(1.0, 1.02, 1.05); 
    
    float total_weight = 0.0;

    // 螺旋采样
    for(int i = 0; i < SAMPLES; i++) {
        float f_i = float(i);
        float progress = f_i / float(SAMPLES);
        
        float weight = exp(-progress * 3.0); 
        
        // 旋转角度，偏移
        float angle = f_i * GOLDEN_ANGLE;
        float curr_radius = progress * radius;
        vec2 offset = vec2(cos(angle), sin(angle)) * curr_radius;

        // 分通道色散
        float r = soft_threshold(texture(fbo, v_texcoord + offset * chromatic_weights.r).rgb, threshold).r;
        float g = soft_threshold(texture(fbo, v_texcoord + offset * chromatic_weights.g).rgb, threshold).g;
        float b = soft_threshold(texture(fbo, v_texcoord + offset * chromatic_weights.b).rgb, threshold).b;
        
        final_glow += vec3(r, g, b) * weight;
        total_weight += weight;
    }
    
    final_glow /= total_weight;
    final_glow *= intensity;

    if(glow_color.a > 0.0) {
        // Screen
        final_glow *= glow_color.rgb;
    }

    // 防止过曝
    vec3 result = scene_color.rgb + final_glow;

    f_color = vec4(result, clamp(scene_color.a + length(final_glow), 0.0, 1.0));

    #[JA_FINISH_UP]
}
