// float vignette_radius = 0.5;    // 晕影开始点（从中心向外多远开始消失）
// float vignette_softness = 0.4;  // 边缘羽化程度（值越大，消失得越平滑）
// float vignette_intensity = 1.0; // 整体强度
// float aspect_ratio = 1.77;      // 宽高比 (width/height)，用于修正圆形，不修正则为椭圆

vec4 scene_color = texture(fbo, v_texcoord);

// 修正 UV 坐标到中心 (-0.5, 0.5)
vec2 uv = v_texcoord - vec2(0.5);

// 修正宽高比
uv.x *= aspect_ratio;

float dist = length(uv);
float vignette = smoothstep(vignette_radius, vignette_radius - vignette_softness, dist);
float final_alpha = clamp(scene_color.a * vignette * vignette_intensity, 0.0, 1.0);

f_color = vec4(scene_color.rgb, final_alpha);
